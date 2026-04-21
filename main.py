import os
import asyncio
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")


# ---------------- HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 V7 POLLING BOT ONLINE")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")


# ---------------- MAIN BOT ----------------
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot is running (polling mode)...")

    # IMPORTANT: polling mode (no webhook)
    await app.run_polling()


# ---------------- START ----------------
if __name__ == "__main__":
    asyncio.run(run_bot())
