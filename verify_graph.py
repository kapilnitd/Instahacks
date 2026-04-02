"""Verify Instagram Graph API credentials from .env.

Run from the insta_hacks directory:
  python verify_graph.py

Success: prints account id, username, followers_count, media_count (no token output).
Failure: prints Meta error JSON message only.
"""

from __future__ import annotations

import json
import sys

import requests

from src.config import get_settings
from src.instagram_client import InstagramGraphClient, instagram_graph_base_url


def main() -> int:
    s = get_settings()
    if not s.access_token or not s.business_account_id:
        print(
            "FAIL: set INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_BUSINESS_ACCOUNT_ID in .env",
            file=sys.stderr,
        )
        return 1
    try:
        client = InstagramGraphClient(s.access_token, s.business_account_id)
        data = client.get_account_overview()
    except requests.HTTPError as e:
        resp = e.response
        status = getattr(resp, "status_code", None) if resp is not None else None
        body = resp.text if resp is not None else ""
        try:
            err = json.loads(body).get("error", {})
            msg = err.get("message", body[:500])
            code = err.get("code", "")
        except json.JSONDecodeError:
            msg, code = body[:500], ""
        print(f"FAIL: HTTP {status if status is not None else '?'}" + (f" (code {code})" if code != "" else ""))
        print(f"Meta says: {msg}")
        return 2
    print("OK: Graph API connection successful.")
    print(f"  api_base: {instagram_graph_base_url()}")
    print(f"  id: {data.get('id')}")
    print(f"  username: {data.get('username')}")
    print(f"  followers_count: {data.get('followers_count')}")
    print(f"  media_count: {data.get('media_count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
