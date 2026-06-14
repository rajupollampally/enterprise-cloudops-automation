import argparse
import logging
import os
import time
from typing import Optional

import schedule
import yaml

import health.collectors as health_collectors
import health.analyzer as health_analyzer
import reporter
import waste.collectors as waste_collectors
import waste.analyzer as waste_analyzer
from collector_utils import request_json

logger = logging.getLogger(__name__)


def load_config(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as handle:
        return yaml.safe_load(handle)


def collect_cluster_data(env_cfg: dict, cluster_name: str) -> dict:
    return health_collectors.collect_cluster_health(env_cfg, cluster_name)


def collect_cloud_waste(env_cfg: dict) -> dict:
    return waste_collectors.collect_cloud_waste(env_cfg)


def run_for_environment(config: dict, environment: str, cluster_name: Optional[str] = None):
    env_cfg = config['environments'][environment]
    clusters = [cluster_name] if cluster_name else env_cfg.get('clusters', [])

    if not clusters:
        logger.warning('No clusters configured for environment %s', environment)
        return

    cluster_data = []
    for cluster in clusters:
        logger.info('Collecting data for %s / %s', environment, cluster)
        cluster_data.append(collect_cluster_data(env_cfg, cluster))

    cloud_waste = collect_cloud_waste(env_cfg)
    waste_df = waste_analyzer.analyze_waste(
        cloud_waste.get('storage', {}).get('storage', []),
        cloud_waste.get('vms', {}).get('vms', []),
        config['report'].get('storage_report_threshold_gb', 5),
    )
    health_summary = health_analyzer.build_health_summary(cluster_data)
    reporter.send_reports(config, environment, health_summary, waste_df, cloud_waste)


def run_all_environments(config: dict, cluster_name: Optional[str] = None):
    for environment in config['environments'].keys():
        run_for_environment(config, environment, cluster_name)


def main():
    parser = argparse.ArgumentParser(description='Daily Kubernetes monitoring and waste reporting')
    parser.add_argument('--env', choices=['dev', 'prod', 'all'], default='dev', help='Environment to report on')
    parser.add_argument('--cluster', help='Optional single cluster name to collect')
    parser.add_argument('--config', default=os.path.join(os.path.dirname(__file__), 'config.yaml'), help='Path to config.yaml')
    parser.add_argument('--loop', action='store_true', help='Run once per day in a loop')
    parser.add_argument('--run-at', default='06:00', help='Daily run time when --loop is enabled')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    config = load_config(args.config)

    if args.loop:
        if args.env == 'all':
            schedule.every().day.at(args.run_at).do(run_all_environments, config, args.cluster)
        else:
            schedule.every().day.at(args.run_at).do(run_for_environment, config, args.env, args.cluster)
        logger.info('Scheduler started for %s, run time %s', args.env, args.run_at)
        while True:
            schedule.run_pending()
            time.sleep(30)
    else:
        if args.env == 'all':
            run_all_environments(config, args.cluster)
        else:
            run_for_environment(config, args.env, args.cluster)


if __name__ == '__main__':
    main()
