# Kubernetes Monitoring Health

This folder contains health monitoring logic for Kubernetes clusters.

## Files

- `collectors.py` - collects monitoring data from Splunk, Prometheus, Grafana, Dynatrace, and Datadog.
- `analyzer.py` - analyzes alerting, restart, and cluster health summaries.

## Usage

Use `monitoring/run_daily.py` to run the health collection and reporting workflow.
