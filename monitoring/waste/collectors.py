import logging
from typing import Any, Dict

from collector_utils import request_json

logger = logging.getLogger(__name__)


def collect_azure_waste(config: Dict[str, Any]) -> Dict[str, Any]:
    if not config.get('cost_api_url'):
        logger.warning('Azure waste collection is not configured.')
        return {}

    url = config['cost_api_url']
    headers = {'Authorization': f"Bearer {config.get('api_token', '')}"}
    params = {'interval': '7d', 'threshold_gb': config.get('storage_threshold_gb', 5)}
    return request_json(url, headers=headers, params=params)


def collect_cloud_waste(env_cfg: Dict[str, Any]) -> Dict[str, Any]:
    azure_cfg = env_cfg.get('azure', {})
    return {
        'storage': request_json(azure_cfg.get('waste_api_url', '')) if azure_cfg.get('waste_api_url') else {},
        'vms': request_json(azure_cfg.get('idle_vm_api_url', '')) if azure_cfg.get('idle_vm_api_url') else {},
    }
