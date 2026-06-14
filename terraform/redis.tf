resource "azurerm_redis_cache" "primary" {
  name                = "${var.prefix}-redis-pri"
  location            = azurerm_virtual_network.primary.location
  resource_group_name = azurerm_resource_group.main.name
  capacity            = 1
  family              = "P"
  sku_name            = "Premium"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
  redis_configuration = {
    maxclients = "2000"
  }
  tags = local.common_tags
}

resource "azurerm_redis_cache" "secondary" {
  name                = "${var.prefix}-redis-sec"
  location            = azurerm_virtual_network.secondary.location
  resource_group_name = azurerm_resource_group.main.name
  capacity            = 1
  family              = "P"
  sku_name            = "Premium"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
  redis_configuration = {
    maxclients = "2000"
  }
  tags = local.common_tags
}

resource "azurerm_redis_linked_server" "redis_dr" {
  name                     = "${var.prefix}-redis-link"
  resource_group_name      = azurerm_resource_group.main.name
  primary_redis_cache_id   = azurerm_redis_cache.primary.id
  secondary_redis_cache_id = azurerm_redis_cache.secondary.id
  replication_role         = "Secondary"
  depends_on = [azurerm_redis_cache.primary, azurerm_redis_cache.secondary]
}
