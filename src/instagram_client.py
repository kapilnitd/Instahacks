from typing import Any, Dict

import requests


class InstagramGraphClient:
    BASE_URL = "https://graph.facebook.com/v21.0"

    def __init__(self, access_token: str, business_account_id: str) -> None:
        self.access_token = access_token
        self.business_account_id = business_account_id

    def get_account_overview(self) -> Dict[str, Any]:
        """Fetch basic account metadata using official Graph API."""
        endpoint = f"{self.BASE_URL}/{self.business_account_id}"
        params = {
            "fields": "id,username,followers_count,media_count",
            "access_token": self.access_token,
        }
        resp = requests.get(endpoint, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
