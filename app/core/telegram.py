import httpx

from app.core.config import settings


def send_telegram_alert(text: str) -> None:
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"  # noqa
    payload = {
        "chat_id": settings.telegram_chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    try:
        response = httpx.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"[TELEGRAM ERROR]: {e}")
