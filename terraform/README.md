# Terraform for Azure IaaS

This Terraform module deploys a private, multi-region Azure infrastructure for production and non-production use.

## Terraform file structure

- `provider.tf` - Azure provider configuration.
- `locals.tf` - common tags and metadata.
- `resource_group.tf` - resource group provisioning.
- `network.tf` - virtual networks, subnets, NSGs, and private networking.
- `sql.tf` - private Azure SQL Server primary/secondary and failover group.
- `redis.tf` - private Azure Redis Cache primary/secondary and DR replication.
- `private_dns.tf` - private DNS zones and private endpoints for SQL and Redis.
- `aks.tf` - three private AKS clusters across primary, secondary, and tertiary regions.
- `outputs.tf` - export useful resource endpoints and IDs.
- `variables.tf` - input variables for reusable configuration.
- `environments/` - environment-specific variable sets for `prod` and `nonprod`.

## Usage

Use the environment files to apply reusable prod/nonprod deployments.

Example for production:

```powershell
cd terraform
terraform init
terraform plan -var-file=environments/prod.tfvars
terraform apply -var-file=environments/prod.tfvars
```

Example for non-production:

```powershell
terraform plan -var-file=environments/nonprod.tfvars
terraform apply -var-file=environments/nonprod.tfvars
```

## Sensitive values

Provide sensitive values securely:

- `ARM_CLIENT_ID`
- `ARM_CLIENT_SECRET`
- `ARM_TENANT_ID`
- `ARM_SUBSCRIPTION_ID`
- `TF_VAR_sql_admin_password`

## Notes for teammates

- The module is intentionally split across resource domains for readability and reuse.
- `environments/*.tfvars` captures environment-specific differences like region, node count, and naming.
- All SQL and Redis resources are private and use private endpoints.
- AKS clusters are private clusters; the API server is not publicly accessible.
