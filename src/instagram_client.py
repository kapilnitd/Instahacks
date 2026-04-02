import os
from typing import Any, Dict

import requests

# Instagram Login app tokens call graph.instagram.com. Facebook Login + Page-linked
# setups often use graph.facebook.com. Override with INSTAGRAM_GRAPH_BASE_URL if needed.
_DEFAULT_BASE = "https://graph.instagram.com/v21.0"


def _graph_base_url() -> str:
    return (os.getenv("INSTAGRAM_GRAPH_BASE_URL") or _DEFAULT_BASE).rstrip("/")


def instagram_graph_base_url() -> str:
    """Resolved Graph API host (for diagnostics)."""
    return _graph_base_url()


class InstagramGraphClient:
    def __init__(self, access_token: str, business_account_id: str) -> None:
        self.access_token = access_token
        self.business_account_id = business_account_id

    def get_account_overview(self) -> Dict[str, Any]:
        """Fetch basic account metadata using official Instagram Graph API."""
        endpoint = f"{_graph_base_url()}/{self.business_account_id}"
        params = {
            "fields": "id,username,followers_count,media_count",
            "access_token": self.access_token,
        }
        resp = requests.get(endpoint, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
