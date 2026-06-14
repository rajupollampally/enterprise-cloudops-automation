import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

from collector_utils import request_json

logger = logging.getLogger(__name__)


def collect_splunk_alerts(config: Dict[str, Any], cluster_name: str) -> Dict[str, Any]:
    url = f"{config['base_url'].rstrip('/')}/services/search/jobs"
    headers = {'Authorization': f"Bearer {config['token']}"}
    query = (
        'search index=main (severity=high OR severity=critical OR severity=error) '
        f'cluster="{cluster_name}" | stats count by host, sourcetype, severity'
    )
    params = {'search': query, 'output_mode': 'json'}
    return request_json(url, headers=headers, params=params)


def collect_prometheus_metrics(config: Dict[str, Any], cluster_name: str) -> Dict[str, Any]:
    now = int(datetime.utcnow().timestamp())
    start = now - 86400
    url = f"{config['base_url'].rstrip('/')}/api/v1/query_range"
    queries = {
        'container_restarts': 'increase(kube_pod_container_status_restarts_total[24h])',
        'node_ready': 'sum(kube_node_status_condition{condition="Ready",status="true",cluster="%s"}) by (cluster)' % cluster_name,
        'db_connection_errors': 'sum(rate(pg_stat_activity_errors_total[1h])) by (cluster)',
    }
    data = {}
    for metric, expr in queries.items():
        params = {'query': expr, 'start': start, 'end': now, 'step': 3600}
        data[metric] = request_json(url, params=params)
    return data


def collect_grafana_dashboard(config: Dict[str, Any], dashboard_uid: str) -> Dict[str, Any]:
    url = f"{config['base_url'].rstrip('/')}/api/dashboards/uid/{dashboard_uid}"
    headers = {'Authorization': f"Bearer {config['api_key']}"}
    return request_json(url, headers=headers)


def collect_dynatrace_problems(config: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{config['base_url'].rstrip('/')}/api/v2/problems"
    headers = {'Authorization': f"Api-Token {config['api_token']}"}
    since = (datetime.utcnow() - timedelta(days=1)).isoformat(timespec='seconds') + 'Z'
    params = {'from': since, 'severity': 'ERROR,PERFORMANCE,AVAILABILITY', 'pageSize': 100}
    return request_json(url, headers=headers, params=params)


def collect_datadog_events(config: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{config['base_url'].rstrip('/')}/api/v1/events"
    headers = {'DD-API-KEY': config['api_key'], 'DD-APPLICATION-KEY': config['app_key']}
    since = int((datetime.utcnow() - timedelta(days=1)).timestamp())
    params = {'start': since, 'priority': 'all', 'sources': 'kubernetes,aws,azure'}
    return request_json(url, headers=headers, params=params)


def collect_cluster_health(config: Dict[str, Any], cluster_name: str) -> Dict[str, Any]:
    return {
        'cluster_name': cluster_name,
        'splunk': collect_splunk_alerts(config['splunk'], cluster_name),
        'prometheus': collect_prometheus_metrics(config['prometheus'], cluster_name),
        'grafana': collect_grafana_dashboard(config['grafana'], config['grafana']['dashboard_uid']),
    }
