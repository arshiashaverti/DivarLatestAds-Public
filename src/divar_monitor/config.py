import os
from dataclasses import dataclass

DEFAULT_URL = (
    "https://divar.ir/s/tehran/game-consoles"
    "?merchandise-type=gaming-controller&status=repair-needed%2C"
)


@dataclass(frozen=True)
class Settings:
    url: str
    state_file: str
    max_ads: int
    wait_ms: int


def load_settings() -> Settings:
    return Settings(
        url=os.getenv("DIVAR_URL", DEFAULT_URL),
        state_file=os.getenv("DIVAR_STATE_FILE", "data/known_ads.json"),
        max_ads=max(1, min(int(os.getenv("DIVAR_MAX_ADS", "10")), 50)),
        wait_ms=max(0, int(os.getenv("DIVAR_WAIT_MS", "4000"))),
    )


def get_telegram_credentials() -> tuple[str, str]:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    missing = []
    if not token:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not chat_id:
        missing.append("TELEGRAM_CHAT_ID")

    if missing:
        raise RuntimeError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    return token, chat_id