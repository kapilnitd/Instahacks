import sys

from src.scheduler import start_scheduler


if __name__ == "__main__":
    # Line-buffer stdout when possible so logs show up under non-TTY runners / IDEs.
    try:
        sys.stdout.reconfigure(line_buffering=True)  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        pass
    start_scheduler()
