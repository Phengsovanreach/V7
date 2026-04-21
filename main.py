import logging
from fastapi import FastAPI, Request

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, WEBHOOK_URL
from router import handle_message
from users import allow_user

logging.basicConfig(level=logging.INFO)

app = FastAPI()

tg_app = ApplicationBuilder().token(BOT_TOKEN).build()


# ---------------- START COMMAND ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 V7 ULTRA PRO ONLINE")


# ---------------- MESSAGE HANDLER ----------------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if not allow_user(user_id):
        await update.message.reply_text("⚠️ Rate limit reached. Try again later.")
        return

    result = await handle_message(text)
    await update.message.reply_text(result)


# ---------------- REGISTER ----------------
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))


# ---------------- WEBHOOK ----------------
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"ok": True}


# ---------------- STARTUP ----------------
@app.on_event("startup")
async def startup():
    logging.info("Setting webhook...")

    await tg_app.bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True
    )

    logging.info("Webhook ready")


# ---------------- ROOT ----------------
@app.get("/")
def home():
    return {"status": "V7 ULTRA PRO ACTIVE"}