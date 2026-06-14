# Jenkins-Driven Azure Deployment UI

This folder contains a Jenkins-focused deployment scaffold with a small UI for team metadata and Azure AD SSO.

## Files

- `Jenkinsfile` - Jenkins pipeline that validates PR approvals and runs Terraform.
- `check_pr_approvals.py` - Python helper to count GitHub PR approvals.
- `slack_notify.py` - Sends success/failure notifications to Slack.
- `build_request_form.html` - UI form for deployment request metadata.
- `trigger_build.js` - Client-side JavaScript for Azure AD sign-in and Jenkins trigger.
- `requirements.txt` - Python dependencies.

## Setup

1. Deploy `build_request_form.html` and `trigger_build.js` to a static web host or Jenkins web server.
2. Register an Azure AD app and set `clientId` in `trigger_build.js`.
3. Configure Jenkins to expose a POST endpoint at `/jenkins/trigger` that accepts metadata and triggers the pipeline.
4. Add Jenkins credentials for `azure-service-principal`, `github-token`, and `slack-webhook`.
5. Install Python `requests` in Jenkins agent environment.
