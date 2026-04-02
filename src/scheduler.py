import random
import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import get_settings



def _manual_action_prompt() -> None:
    # Intentional manual step: no automated engagement actions.
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Reminder: review hashtag/topic feed manually and take compliant actions.")



def start_scheduler() -> None:
    settings = get_settings()
    scheduler = BlockingScheduler()

    # Randomized minute jitter only for reminders.
    for hour in range(settings.min_hour, settings.max_hour + 1):
        if random.random() < 0.45:
            minute = random.randint(0, 59)
            scheduler.add_job(_manual_action_prompt, "cron", hour=hour, minute=minute)

    print("Scheduler started. Press Ctrl+C to stop.")
    print(f"Reminder window: {settings.min_hour}:00 to {settings.max_hour}:59")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
        time.sleep(0.2)
