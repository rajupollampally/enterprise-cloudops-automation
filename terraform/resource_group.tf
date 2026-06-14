resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.primary_location
  tags     = local.common_tags
}
