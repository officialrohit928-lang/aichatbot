from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not BOT_TOKEN or not GROQ_API_KEY:
    raise RuntimeError("ENV VARS MISSING")

URL = "https://api.groq.com/openai/v1/chat/completions"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": text}],
        "temperature": 0.7
    }

    try:
        r = requests.post(URL, headers=headers, json=data, timeout=15)
        res = r.json()
        msg = res["choices"][0]["message"]["content"]
    except Exception as e:
        msg = "AI error, try again later."

    await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
