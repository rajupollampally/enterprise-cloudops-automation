# Azure IaaS CI/CD Pipeline Scaffold

This sample workspace provides an Azure infrastructure deployment workflow with:

- Private Azure virtual network architecture
- Azure SQL Server with disaster recovery failover group
- Azure Redis Cache geo-replication for DR
- Three private AKS clusters deployed across three regions for high availability
- Jenkins pipeline enforcing GitHub PR approval gating
- Slack notification integration for success, failure, and error events

## Structure

- `terraform/` - Terraform configuration for Azure resources
- `jenkins/` - Jenkins pipeline and Slack notification helper

## Next steps

1. Customize `terraform/variables.tf` values and secure secrets.
2. Configure Jenkins credentials for Azure and Slack.
3. Configure GitHub token for PR approval checks.
4. Deploy the Terraform workspace from the Jenkins pipeline.
