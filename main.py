import asyncio
import logging
from fastapi import FastAPI

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# ---------------- BOT ----------------
tg_app = ApplicationBuilder().token(BOT_TOKEN).build()


# ---------------- HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 V8 STABLE PRO ONLINE")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# ---------------- BACKGROUND POLLING ----------------
async def bot_worker():
    print("🤖 Bot polling started...")
    await tg_app.initialize()
    await tg_app.start()
    await tg_app.updater.start_polling()


# ---------------- FASTAPI START ----------------
@app.on_event("startup")
async def startup():
    asyncio.create_task(bot_worker())


# ---------------- HEALTH CHECK ----------------
@app.get("/")
def home():
    return {"status": "V8 STABLE PRO RUNNING"}
