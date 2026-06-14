import base64
import io
import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


def request_json(url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None, timeout: int = 30):
    if not url:
        logger.warning('request_json called with empty URL')
        return {}

    try:
        response = requests.get(url, headers=headers or {}, params=params or {}, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        logger.error('Request failed for %s: %s', url, exc)
        return {}


def post_json(url: str, headers: Optional[Dict[str, str]] = None, payload: Optional[Dict[str, Any]] = None, timeout: int = 30):
    if not url:
        logger.warning('post_json called with empty URL')
        return {}

    try:
        response = requests.post(url, headers=headers or {}, json=payload or {}, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        logger.error('POST failed for %s: %s', url, exc)
        return {}


def render_plot_base64(figure) -> str:
    buffer = io.BytesIO()
    figure.tight_layout()
    figure.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode('ascii')
    return f'data:image/png;base64,{encoded}'
