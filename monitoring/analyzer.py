import pandas as pd
from datetime import datetime
from typing import Any, Dict, List


def extract_splunk_alerts(splunk_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    results = []
    for item in splunk_payload.get('results', []):
        results.append({
            'host': item.get('host'),
            'sourcetype': item.get('sourcetype'),
            'severity': item.get('severity'),
            'count': int(item.get('count', 0)),
        })
    return results


def count_prometheus_events(prometheus_payload: Dict[str, Any]) -> Dict[str, int]:
    counts = {'restarts': 0, 'node_ready': 0, 'db_errors': 0}
    for metric in ['container_restarts', 'node_ready', 'db_connection_errors']:
        data = prometheus_payload.get(metric, {}).get('data', {})
        for result in data.get('result', []):
            if metric == 'container_restarts':
                value = int(float(result.get('values', [[0, 0]])[-1][1]))
                counts['restarts'] += value
            elif metric == 'node_ready':
                counts['node_ready'] += 1
            elif metric == 'db_connection_errors':
                value = int(float(result.get('values', [[0, 0]])[-1][1]))
                counts['db_errors'] += value
    return counts


def build_monitoring_summary(cluster_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    alert_rows = []
    restart_rows = []
    problem_rows = []
    for cluster in cluster_data:
        cluster_name = cluster.get('cluster_name')
        splunk_alerts = extract_splunk_alerts(cluster['splunk'])
        prometheus_counts = count_prometheus_events(cluster['prometheus'])

        for alert in splunk_alerts:
            alert_rows.append({
                'cluster': cluster_name,
                'host': alert['host'],
                'sourcetype': alert['sourcetype'],
                'severity': alert['severity'],
                'count': alert['count'],
            })

        restart_rows.append({
            'cluster': cluster_name,
            'restarts': prometheus_counts['restarts'],
            'db_errors': prometheus_counts['db_errors'],
            'node_ready_metrics': prometheus_counts['node_ready'],
        })

    alerts_df = pd.DataFrame(alert_rows)
    restarts_df = pd.DataFrame(restart_rows)

    critical_alerts = alerts_df[alerts_df['severity'].isin(['critical', 'CRITICAL', 'error', 'ERROR'])]
    red_alerts = critical_alerts.groupby('cluster').sum().reset_index() if not critical_alerts.empty else pd.DataFrame()

    return {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'cluster_count': len(cluster_data),
        'alerts': alerts_df,
        'restarts': restarts_df,
        'critical_alerts': critical_alerts,
        'red_alerts': red_alerts,
    }


def analyze_waste(storage_report: Dict[str, Any], vm_report: Dict[str, Any], threshold_gb: int) -> pd.DataFrame:
    rows = []
    for item in storage_report.get('storage', []):
        if item.get('unused_gb', 0) >= threshold_gb:
            rows.append({
                'resource_id': item.get('resource_id'),
                'resource_type': 'storage',
                'owner': item.get('owner'),
                'environment': item.get('environment'),
                'unused_gb': item.get('unused_gb'),
                'reason': item.get('reason', 'Unused storage'),
            })

    for vm in vm_report.get('vms', []):
        if not vm.get('in_use', True):
            rows.append({
                'resource_id': vm.get('resource_id'),
                'resource_type': 'vm',
                'owner': vm.get('owner'),
                'environment': vm.get('environment'),
                'unused_gb': vm.get('estimated_cost_gb', 0),
                'reason': vm.get('reason', 'Idle VM'),
            })

    waste_df = pd.DataFrame(rows)
    if not waste_df.empty and 'owner' in waste_df.columns:
        waste_df['owner'] = waste_df['owner'].fillna('unknown')
    return waste_df


def summarize_waste_report(waste_df: pd.DataFrame) -> Dict[str, Any]:
    if waste_df.empty:
        return {'total_items': 0, 'total_unused_gb': 0, 'top_risks': []}

    summary = {
        'total_items': len(waste_df),
        'total_unused_gb': int(waste_df['unused_gb'].sum()),
        'top_risks': waste_df.sort_values('unused_gb', ascending=False).head(10).to_dict(orient='records'),
    }
    return summary
