import os
import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

app = FastAPI()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")

tg_app = ApplicationBuilder().token(BOT_TOKEN).build()


# ---------------- AUTO WEBHOOK SETUP ----------------
def get_base_url():
    """
    Auto-detect Render URL or external host
    """
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    
    if render_url:
        return render_url

    # fallback (local)
    return os.environ.get("BASE_URL", "http://localhost:10000")


@app.on_event("startup")
async def startup():
    base_url = get_base_url()
    webhook_url = f"{base_url}/webhook"

    logging.info(f"🌐 Setting webhook: {webhook_url}")

    await tg_app.bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True
    )

    logging.info("✅ Webhook auto-configured")


# ---------------- WEBHOOK ENDPOINT ----------------
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"ok": True}
