variable "prefix" {
  description = "Prefix for naming Azure resources"
  type        = string
  default     = "iaas"
}

variable "resource_group_name" {
  description = "Azure resource group name"
  type        = string
  default     = "iaas-rg"
}

variable "primary_location" {
  description = "Primary Azure region"
  type        = string
  default     = "eastus"
}

variable "secondary_location" {
  description = "Secondary Azure region for DR resources"
  type        = string
  default     = "eastus2"
}

variable "tertiary_location" {
  description = "Tertiary Azure region for additional DR/cluster resources"
  type        = string
  default     = "centralus"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "prod"
}

variable "team_name" {
  description = "Team name owning the deployment"
  type        = string
  default     = "PlatformTeam"
}

variable "team_budget_id" {
  description = "Team budget ID"
  type        = string
  default     = "BUDGET-001"
}

variable "team_vip" {
  description = "Team VIP contact"
  type        = string
  default     = "vip@example.com"
}

variable "team_lead" {
  description = "Team lead name"
  type        = string
  default     = "Team Lead"
}

variable "product" {
  description = "Product that owns the deployment"
  type        = string
  default     = "CoreProduct"
}

variable "aks_node_count" {
  description = "Number of nodes in each AKS cluster node pool"
  type        = number
  default     = 4
}

variable "aks_node_vm_size" {
  description = "VM size used by AKS nodes"
  type        = string
  default     = "Standard_D4s_v3"
}

variable "sql_admin_login" {
  description = "SQL administrator login name"
  type        = string
  default     = "sqladminuser"
}

variable "sql_admin_password" {
  description = "SQL administrator password"
  type        = string
  sensitive   = true
}

variable "sql_database_name" {
  description = "Primary SQL database name"
  type        = string
  default     = "appdb"
}

variable "slack_channel" {
  description = "Slack channel or webhook tag for notifications"
  type        = string
  default     = "#deployments"
}
