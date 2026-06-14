resource "azurerm_private_dns_zone" "sql" {
  name                = "privatelink.database.windows.net"
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_private_dns_zone" "redis" {
  name                = "privatelink.redis.cache.windows.net"
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "sql_primary_vnet" {
  name                  = "${var.prefix}-sql-primary-link"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.sql.name
  virtual_network_id    = azurerm_virtual_network.primary.id
}

resource "azurerm_private_dns_zone_virtual_network_link" "redis_primary_vnet" {
  name                  = "${var.prefix}-redis-primary-link"
  resource_group_name   = azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.redis.name
  virtual_network_id    = azurerm_virtual_network.primary.id
}

resource "azurerm_private_endpoint" "sql_primary_pe" {
  name                = "${var.prefix}-sql-pri-pe"
  location            = azurerm_virtual_network.primary.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.pe_primary.id

  private_service_connection {
    name                           = "sql-primary-psc"
    private_connection_resource_id = azurerm_mssql_server.primary.id
    is_manual_connection           = false
    subresource_names              = ["sqlServer"]
  }
}

resource "azurerm_private_endpoint" "sql_secondary_pe" {
  name                = "${var.prefix}-sql-sec-pe"
  location            = azurerm_virtual_network.secondary.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.pe_secondary.id

  private_service_connection {
    name                           = "sql-secondary-psc"
    private_connection_resource_id = azurerm_mssql_server.secondary.id
    is_manual_connection           = false
    subresource_names              = ["sqlServer"]
  }
}

resource "azurerm_private_endpoint" "redis_primary_pe" {
  name                = "${var.prefix}-redis-pri-pe"
  location            = azurerm_virtual_network.primary.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.pe_primary.id

  private_service_connection {
    name                           = "redis-primary-psc"
    private_connection_resource_id = azurerm_redis_cache.primary.id
    is_manual_connection           = false
    subresource_names              = ["redisCache"]
  }
}

resource "azurerm_private_endpoint" "redis_secondary_pe" {
  name                = "${var.prefix}-redis-sec-pe"
  location            = azurerm_virtual_network.secondary.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.pe_secondary.id

  private_service_connection {
    name                           = "redis-secondary-psc"
    private_connection_resource_id = azurerm_redis_cache.secondary.id
    is_manual_connection           = false
    subresource_names              = ["redisCache"]
  }
}
