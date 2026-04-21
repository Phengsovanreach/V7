import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")

if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL missing")