resource "azurerm_mssql_server" "primary" {
  name                         = "${var.prefix}-sql-pri"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = var.primary_location
  version                      = "12.0"
  administrator_login          = var.sql_admin_login
  administrator_login_password = var.sql_admin_password
  public_network_access_enabled = false
  minimal_tls_version          = "1.2"
  tags                         = local.common_tags
}

resource "azurerm_mssql_server" "secondary" {
  name                         = "${var.prefix}-sql-sec"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = var.secondary_location
  version                      = "12.0"
  administrator_login          = var.sql_admin_login
  administrator_login_password = var.sql_admin_password
  public_network_access_enabled = false
  minimal_tls_version          = "1.2"
  tags                         = local.common_tags
}

resource "azurerm_mssql_database" "primary_db" {
  name       = var.sql_database_name
  server_id  = azurerm_mssql_server.primary.id
  sku_name   = "S2"
  max_size_gb = 10
  tags       = local.common_tags
}

resource "azurerm_mssql_database" "secondary_db" {
  name                           = var.sql_database_name
  server_id                      = azurerm_mssql_server.secondary.id
  create_mode                    = "Secondary"
  create_mode_source_database_id = azurerm_mssql_database.primary_db.id
  tags                           = local.common_tags
}

resource "azurerm_mssql_failover_group" "sql_dr" {
  name                = "${var.prefix}-sql-failover"
  resource_group_name = azurerm_resource_group.main.name
  server_id           = azurerm_mssql_server.primary.id
  partner_server_id   = azurerm_mssql_server.secondary.id

  read_write_endpoint_failover_policy {
    mode          = "Automatic"
    grace_minutes = 60
  }

  read_only_endpoint_failover_policy {
    mode = "Enabled"
  }

  databases = [azurerm_mssql_database.primary_db.id]
  tags      = local.common_tags
}
