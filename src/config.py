import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    access_token: str
    business_account_id: str
    min_hour: int
    max_hour: int



def get_settings() -> Settings:
    return Settings(
        access_token=os.getenv("INSTAGRAM_ACCESS_TOKEN", ""),
        business_account_id=os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", ""),
        min_hour=int(os.getenv("SCHEDULER_MIN_HOUR", "9")),
        max_hour=int(os.getenv("SCHEDULER_MAX_HOUR", "21")),
    )
