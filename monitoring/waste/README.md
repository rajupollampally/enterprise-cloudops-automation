# Kubernetes Waste Reporting

This folder contains waste and cost optimization logic for Azure and Kubernetes resources.

## Files

- `collectors.py` - collects waste data from Azure storage and idle VM endpoints.
- `analyzer.py` - analyzes waste and generates cost-saving recommendations.

## Usage

Use `monitoring/run_daily.py` to run the waste collection and reporting workflow.
