import pandas as pd
from typing import Any, Dict


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
