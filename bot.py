from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ✅ safety check
    if not update.message or not update.message.text:
        return  # non-text message ignore

    user_text = update.message.text.strip()

    if not user_text:
        return  # empty message ignore

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "user", "content": user_text}
    ]
    }

    r = requests.post(URL, headers=headers, json=payload, timeout=20)

    # 👇 DEBUG (VERY IMPORTANT)
    if r.status_code != 200:
        await update.message.reply_text(
            f"Groq API error {r.status_code}\n{r.text}"
        )
        return

    data = r.json()
    reply_text = data["choices"][0]["message"]["content"]
    await update.message.reply_text(reply_text)
    
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
