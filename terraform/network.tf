resource "azurerm_virtual_network" "primary" {
  name                = "${var.prefix}-vnet-primary"
  location            = var.primary_location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.0.0.0/16"]
  tags                = local.common_tags
}

resource "azurerm_virtual_network" "secondary" {
  name                = "${var.prefix}-vnet-secondary"
  location            = var.secondary_location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.1.0.0/16"]
  tags                = local.common_tags
}

resource "azurerm_virtual_network" "tertiary" {
  name                = "${var.prefix}-vnet-tertiary"
  location            = var.tertiary_location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = ["10.2.0.0/16"]
  tags                = local.common_tags
}

resource "azurerm_subnet" "aks_primary" {
  name                 = "aks-primary-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.primary.name
  address_prefixes     = ["10.0.1.0/24"]
  delegation {
    name = "aksdelegation"
    service_delegation {
      name = "Microsoft.ContainerService/managedClusters"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "aks_secondary" {
  name                 = "aks-secondary-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.secondary.name
  address_prefixes     = ["10.1.1.0/24"]
  delegation {
    name = "aksdelegation"
    service_delegation {
      name = "Microsoft.ContainerService/managedClusters"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "aks_tertiary" {
  name                 = "aks-tertiary-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.tertiary.name
  address_prefixes     = ["10.2.1.0/24"]
  delegation {
    name = "aksdelegation"
    service_delegation {
      name = "Microsoft.ContainerService/managedClusters"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "sql_primary" {
  name                 = "sql-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.primary.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_subnet" "redis_primary" {
  name                 = "redis-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.primary.name
  address_prefixes     = ["10.0.3.0/24"]
}

resource "azurerm_subnet" "pe_primary" {
  name                 = "private-endpoint-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.primary.name
  address_prefixes     = ["10.0.10.0/27"]
}

resource "azurerm_subnet" "pe_secondary" {
  name                 = "private-endpoint-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.secondary.name
  address_prefixes     = ["10.1.10.0/27"]
}

resource "azurerm_subnet" "pe_tertiary" {
  name                 = "private-endpoint-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.tertiary.name
  address_prefixes     = ["10.2.10.0/27"]
}

resource "azurerm_network_security_group" "sql_redis_nsg" {
  name                = "${var.prefix}-sql-redis-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  security_rule {
    name                       = "AllowInternalTraffic"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_address_prefix      = "VirtualNetwork"
    destination_address_prefix = "VirtualNetwork"
    source_port_range          = "*"
    destination_port_range     = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "sql_nsg" {
  subnet_id                 = azurerm_subnet.sql_primary.id
  network_security_group_id = azurerm_network_security_group.sql_redis_nsg.id
}

resource "azurerm_subnet_network_security_group_association" "redis_nsg" {
  subnet_id                 = azurerm_subnet.redis_primary.id
  network_security_group_id = azurerm_network_security_group.sql_redis_nsg.id
}
