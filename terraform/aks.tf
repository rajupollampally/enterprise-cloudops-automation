resource "azurerm_kubernetes_cluster" "aks_primary" {
  name                = "${var.prefix}-aks-primary"
  location            = var.primary_location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.prefix}-aks-primary"

  default_node_pool {
    name            = "agentpool"
    node_count      = var.aks_node_count
    vm_size         = var.aks_node_vm_size
    vnet_subnet_id  = azurerm_subnet.aks_primary.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin     = "azure"
    network_policy     = "azure"
    dns_service_ip     = "10.0.20.10"
    service_cidr       = "10.0.20.0/24"
    docker_bridge_cidr = "172.17.0.1/16"
  }

  private_cluster_enabled = true
  api_server_authorized_ip_ranges = []
  tags = local.common_tags
}

resource "azurerm_kubernetes_cluster" "aks_secondary" {
  name                = "${var.prefix}-aks-secondary"
  location            = var.secondary_location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.prefix}-aks-secondary"

  default_node_pool {
    name            = "agentpool"
    node_count      = var.aks_node_count
    vm_size         = var.aks_node_vm_size
    vnet_subnet_id  = azurerm_subnet.aks_secondary.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin     = "azure"
    network_policy     = "azure"
    dns_service_ip     = "10.1.20.10"
    service_cidr       = "10.1.20.0/24"
    docker_bridge_cidr = "172.18.0.1/16"
  }

  private_cluster_enabled = true
  api_server_authorized_ip_ranges = []
  tags = local.common_tags
}

resource "azurerm_kubernetes_cluster" "aks_tertiary" {
  name                = "${var.prefix}-aks-tertiary"
  location            = var.tertiary_location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.prefix}-aks-tertiary"

  default_node_pool {
    name            = "agentpool"
    node_count      = var.aks_node_count
    vm_size         = var.aks_node_vm_size
    vnet_subnet_id  = azurerm_subnet.aks_tertiary.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin     = "azure"
    network_policy     = "azure"
    dns_service_ip     = "10.2.20.10"
    service_cidr       = "10.2.20.0/24"
    docker_bridge_cidr = "172.19.0.1/16"
  }

  private_cluster_enabled = true
  api_server_authorized_ip_ranges = []
  tags = local.common_tags
}
