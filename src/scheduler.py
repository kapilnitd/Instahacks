import random
import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import get_settings



def _manual_action_prompt() -> None:
    # Intentional manual step: no automated engagement actions.
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"[{now}] Reminder: review hashtag/topic feed manually and take compliant actions.",
        flush=True,
    )



def start_scheduler() -> None:
    settings = get_settings()
    scheduler = BlockingScheduler()

    # Randomized minute jitter only for reminders.
    jobs_added = 0
    for hour in range(settings.min_hour, settings.max_hour + 1):
        if random.random() < 0.45:
            minute = random.randint(0, 59)
            scheduler.add_job(_manual_action_prompt, "cron", hour=hour, minute=minute)
            jobs_added += 1

    if jobs_added == 0:
        hour = random.randint(settings.min_hour, settings.max_hour)
        minute = random.randint(0, 59)
        scheduler.add_job(_manual_action_prompt, "cron", hour=hour, minute=minute)
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
