locals {
  common_tags = {
    team         = var.team_name
    product      = var.product
    team_lead    = var.team_lead
    team_budget  = var.team_budget_id
    team_vip     = var.team_vip
    environment  = var.environment
  }
}
