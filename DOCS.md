# insta_hacks Documentation

## Overview

`insta_hacks` is a small, intentionally conservative starter project for Instagram-related tooling. It is designed to help you:

1. Read configuration from a local `.env` file
2. Schedule *reminder windows* to review content manually
3. Provide a simple wrapper for official Instagram/Meta Graph API calls (where your token/app permissions allow it)

It is **not** designed to automate engagement (likes/comments/follows) or bypass platform controls. This project focuses on compliant “assist and remind” workflows.

## Main entry point

The runnable entry point is:

`src/main.py`

`src/main.py` starts the reminder scheduler by calling `start_scheduler()` from `src/scheduler.py`.

## Configuration (`src/config.py`)

Configuration is loaded from environment variables using `python-dotenv`:

`load_dotenv()`

The `Settings` dataclass exposes:

* `INSTAGRAM_ACCESS_TOKEN` (string)
* `INSTAGRAM_BUSINESS_ACCOUNT_ID` (string)
* `SCHEDULER_MIN_HOUR` (int, default `9`)
* `SCHEDULER_MAX_HOUR` (int, default `21`)

The helper `get_settings()` returns these values and is used by the scheduler.

## Reminder scheduler (`src/scheduler.py`)

The scheduler uses APScheduler’s `BlockingScheduler` and creates jobs that only print reminders.

Key behavior:

1. Hours covered: from `SCHEDULER_MIN_HOUR` to `SCHEDULER_MAX_HOUR` inclusive
2. For each hour, there is a probability gate: `random.random() < 0.45`
3. If an hour is selected, a specific minute is chosen uniformly from `0..59`
4. A cron job is scheduled to call `_manual_action_prompt()` at that hour/minute

What the reminder does:

* The job prints a timestamp and prompts you to review feed/content manually.
* It explicitly avoids any automated engagement actions.

## Graph API wrapper (`src/instagram_client.py`)

`src/instagram_client.py` contains a small helper class:

`InstagramGraphClient`

It is intended to call official Graph API endpoints using your access token.

The current implemented example is:

* `get_account_overview()` which queries the Graph API for basic metadata

Note: This wrapper is not currently integrated into the scheduler loop; it exists as a utility you can call from your own code.

## Example script: `follower.py`

`follower.py` is an additional example script that demonstrates usage of the third-party `instagrapi` library.

Important notes for documentation/usage:

* This script is **not** invoked by `src/main.py`
* It contains placeholder credentials (`your_username`, `your_password`)
* It includes engagement-like functions (search/like/comment/follow/unfollow)

Because of the above, treat `follower.py` as a sketch/example only, not as a recommended automation workflow.

## Setup & run

1. Create your `.env` from `.env.example`
2. Install dependencies:

   `pip install -r requirements.txt`

3. Run the reminder scheduler from the `insta_hacks` directory:

   `python -m src.main`

Expected console output:

* “Scheduler started. Press Ctrl+C to stop.”
* “Reminder window: <min_hour>:00 to <max_hour>:59”
* Later, scheduled reminder timestamps printed by the cron jobs

## Dependencies

From `requirements.txt`, the project expects:

* `python-dotenv`
* `requests`
* `APScheduler`
* `instagrapi` (used by the example `follower.py`)

## Local-only / excluded content

The repository includes a `.gitignore` that excludes potentially sensitive or noisy runtime content such as:

* `.env`
* `logs/`
* `instagrapi/` (to avoid committing vendored dependencies)

Only the intended source/documentation files are committed.

## Troubleshooting

1. If `python -m src.main` fails with import errors:
   * Ensure you are running from the `insta_hacks` directory (the parent of `src/`)
   * If you still get module issues, run `python src/main.py` and/or adjust `PYTHONPATH`

2. If Graph API calls fail (when you use `InstagramGraphClient`):
   * Verify token validity and required permissions/scopes
   * Confirm the `INSTAGRAM_BUSINESS_ACCOUNT_ID` is correct for your app

## File reference

* `README.md` - short starter description
* `DOCS.md` - detailed documentation
* `DOCUMENTATION.txt` - plain-text mirror of this doc
* `.env.example` - environment variable template
* `requirements.txt` - Python dependencies
* `src/main.py` - entry point for the scheduler
* `src/config.py` - `.env` loader + settings dataclass
* `src/scheduler.py` - reminder scheduling logic
* `src/instagram_client.py` - Graph API helper class
* `follower.py` - example script (not wired to `src/main.py`)

