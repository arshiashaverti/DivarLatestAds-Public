import json
import urllib.error
import urllib.parse
import urllib.request

from .config import get_telegram_credentials


def send_telegram_message(message: str) -> None:
    token, chat_id = get_telegram_credentials()

    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message,
        "disable_web_page_preview": "false",
    }).encode("utf-8")

    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=data,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"Telegram returned HTTP {exc.code}."
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError("Could not connect to Telegram.") from exc

    if not result.get("ok"):
        raise RuntimeError("Telegram did not confirm message delivery.")