# Azure Private Network Deployment Notes

## Overview
This deployment creates a private Azure infrastructure with multi-region disaster recovery and a Jenkins-driven CI/CD flow.

## Architecture
- Private Azure Virtual Network in three regions: primary, secondary, tertiary.
- Three private AKS clusters deployed across these regions, each with multiple worker nodes.
- Each AKS cluster uses a private subnet and a private cluster configuration.
- Azure SQL Server is deployed in primary/secondary pair with an automatic failover group.
- Azure Redis Cache is deployed as a primary and secondary pair with geo-replication.
- Private endpoints and private DNS zones are used for SQL and Redis to ensure traffic stays inside Azure private networking.

## DR and High Availability
- SQL DR is provided by Azure SQL Failover Group across primary and secondary servers.
- Redis DR is provided by Azure Redis linked server replication across primary and secondary caches.
- AKS is spread across three regions, giving 10+ worker nodes across the cluster footprint.

## Jenkins CI/CD
- The Jenkins pipeline validates GitHub PR approvals; it only runs when at least 2 approvals exist.
- Deployment metadata is collected from a UI form and forwarded to Jenkins.
- Slack notifications are sent on success, failure, and warnings.
- No Argo CD is used in this workflow.

## Team Metadata
- Team Name
- Product
- Team Lead
- Team VIP
- Budget ID
- Employee ID (from Azure AD login)
- Environment
- Pull Request URL

## Notes for Teammates
- Use `terraform/` for all infrastructure definitions.
- Use `jenkins/` for pipeline and notification tooling.
- The UI form is a simple frontend to collect metadata and trigger Jenkins.
- All infrastructure is designed to run privately with no public access to SQL/Redis.
