import json
import random
import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import get_settings
from src.instagram_client import InstagramGraphClient, instagram_graph_base_url


def _format_api_error(exc: requests.HTTPError) -> str:
    resp = exc.response
    if resp is None:
        return str(exc)
    try:
        err: Dict[str, Any] = resp.json().get("error", {})
        msg = err.get("message", resp.text[:200])
        code = err.get("code", "")
        return f"{msg}" + (f" (code {code})" if code != "" else "")
    except (json.JSONDecodeError, ValueError, TypeError):
        return resp.text[:200] if resp.text else str(exc)


def start_scheduler() -> None:
    settings = get_settings()
    scheduler = BlockingScheduler()

    ig_client: Optional[InstagramGraphClient] = None
    if settings.access_token and settings.business_account_id:
        ig_client = InstagramGraphClient(settings.access_token, settings.business_account_id)
    else:
        print(
            "Instagram: not configured (set INSTAGRAM_ACCESS_TOKEN and "
            "INSTAGRAM_BUSINESS_ACCOUNT_ID in .env). Reminders only.",
            flush=True,
        )

    def reminder_tick() -> None:
        # Reminder + read-only account snapshot (no likes/comments/follows).
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{now}] Reminder: review hashtag/topic feed manually and take compliant actions.",
            flush=True,
        )
        if ig_client is None:
            return
        try:
            data = ig_client.get_account_overview()
            print(
                f"[{now}] Instagram @{data.get('username')} — "
                f"followers: {data.get('followers_count')}, media: {data.get('media_count')}",
                flush=True,
            )
        except requests.HTTPError as e:
            print(f"[{now}] Instagram API error: {_format_api_error(e)}", flush=True)

    if ig_client is not None:
        try:
            preview = ig_client.get_account_overview()
            print(
                f"Instagram: connected via {instagram_graph_base_url()} as "
                f"@{preview.get('username')} (id {preview.get('id')}).",
                flush=True,
            )
        except requests.HTTPError as e:
            print(f"Instagram: startup check failed — {_format_api_error(e)}", flush=True)
            print(
                "Scheduler will still run; each tick will retry the API.",
                flush=True,
            )

    # Randomized minute jitter only for reminders.
    jobs_added = 0
    for hour in range(settings.min_hour, settings.max_hour + 1):
        if random.random() < 0.45:
            minute = random.randint(0, 59)
            scheduler.add_job(reminder_tick, "cron", hour=hour, minute=minute)
            jobs_added += 1

    if jobs_added == 0:
        hour = random.randint(settings.min_hour, settings.max_hour)
        minute = random.randint(0, 59)
        scheduler.add_job(reminder_tick, "cron", hour=hour, minute=minute)
        jobs_added = 1
        print(
            "No random slots rolled; added 1 fallback reminder in the window.",
            flush=True,
        )

    print("Scheduler started. Press Ctrl+C to stop.", flush=True)
    print(
        f"Reminder window: {settings.min_hour}:00 to {settings.max_hour}:59 "
        f"({jobs_added} job(s) scheduled).",
        flush=True,
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.", flush=True)
        time.sleep(0.2)
