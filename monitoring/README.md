# Kubernetes Monitoring and Waste Reporting

This module provides a daily reporting pipeline for large-scale Kubernetes environments, including:

- Splunk alerts and Grafana dashboard health
- Prometheus cluster metrics and container restart trends
- Dynatrace problem detection and Datadog event notifications
- Azure storage and VM waste analysis
- Outlook email and Teams webhook notifications per environment

## Files

- `config.yaml` - environment endpoints, credentials, recipients, and thresholds
- `collectors.py` - collects data from monitoring APIs and Azure waste endpoints
- `analyzer.py` - analyzes cluster health, red alerts, and resource waste
- `reporter.py` - renders HTML reports and sends Outlook/Teams notifications
- `run_daily.py` - CLI entrypoint for one-off or scheduled daily runs
- `templates/` - HTML report templates

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure `config.yaml` with environment-specific API URLs, tokens, email addresses, and webhooks.

3. Optionally set SMTP environment variables:
   - `SMTP_HOST`
   - `SMTP_PORT`

4. Run once:
   ```bash
   python run_daily.py --env dev
   ```

5. Run daily in a loop at 06:00 AM:
   ```bash
   python run_daily.py --env prod --loop --run-at 06:00
   ```

6. Run all configured environments each day at 06:00 AM:
   ```bash
   python run_daily.py --env all --loop --run-at 06:00
   ```

## Notes

- The current implementation supports dev and prod environments with separate report recipients.
- Add more clusters under each environment in `config.yaml`.
- For production, replace sample API endpoints and tokens with your real monitoring service values.
