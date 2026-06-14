# Terraform Environments

This folder contains environment-specific variable sets for the Terraform module.

## Files

- `prod.tfvars` - production deployment values
- `nonprod.tfvars` - non-production deployment values

## How to use

```
terraform plan -var-file=environments/prod.tfvars
terraform apply -var-file=environments/prod.tfvars
```

or:

```
terraform plan -var-file=environments/nonprod.tfvars
terraform apply -var-file=environments/nonprod.tfvars
```

## Why this structure

- Keeps environment-specific naming, region, and sizing settings separate from the reusable core module.
- Makes it easy to add new environments such as `qa.tfvars`, `staging.tfvars`, or `dev.tfvars`.
