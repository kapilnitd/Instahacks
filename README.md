# insta_hacks (Compliant Starter)

This project is a safe starter for Instagram workflow automation using official APIs.

## Important limits

This scaffold does **not** implement:
- automated likes/comments/follows
- login automation by browser scripting
- anti-detection/evasion behavior

Those patterns violate platform rules and can get accounts restricted.

## What it does

- loads API credentials from `.env`
- schedules irregular reminder windows for manual actions
- provides a small SDK-style client wrapper for official Instagram Graph API calls

## Setup

1. Create env file:
   - copy `.env.example` to `.env`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run:
   - `python -m src.main`

## Notes

Use this project for compliant tasks like content planning, inbox/reply assistance on your own assets, and analytics retrieval where your token permissions allow it.
