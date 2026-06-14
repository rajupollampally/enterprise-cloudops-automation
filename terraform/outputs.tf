output "resource_group" {
  description = "Resource group name"
  value       = azurerm_resource_group.main.name
}

output "sql_primary_server" {
  description = "Primary SQL server fully qualified domain name"
  value       = azurerm_mssql_server.primary.fully_qualified_domain_name
}

output "sql_failover_group_id" {
  description = "SQL failover group ID"
  value       = azurerm_mssql_failover_group.sql_dr.id
}

output "redis_primary_host" {
  description = "Primary Redis cache host name"
  value       = azurerm_redis_cache.primary.hostname
}

output "redis_secondary_host" {
  description = "Secondary Redis cache host name"
  value       = azurerm_redis_cache.secondary.hostname
}
