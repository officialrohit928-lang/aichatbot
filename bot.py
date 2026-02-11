from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        r = requests.post(URL, headers=headers, json=payload, timeout=20)

        if r.status_code != 200:
            await update.message.reply_text(
                f"Groq API error: {r.status_code}"
            )
            return

        data = r.json()

        if "choices" not in data:
            await update.message.reply_text("Groq se response nahi mila.")
            return

        reply_text = data["choices"][0]["message"]["content"]
        await update.message.reply_text(reply_text)

    except Exception as e:
        await update.message.reply_text("AI error (exception).")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
