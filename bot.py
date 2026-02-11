from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

# simple memory (per user)
user_memory = {}

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()
    user_id = update.message.from_user.id

    if not user_text:
        return

    # memory init
    if user_id not in user_memory:
        user_memory[user_id] = []

    # last 6 messages hi rakhenge (context limit)
    user_memory[user_id].append({"role": "user", "content": user_text})
    user_memory[user_id] = user_memory[user_id][-6:]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a ChatGPT-like AI assistant. "
                    "Reply exactly according to the user's question. "
                    "Be clear, logical, and helpful. "
                    "Do NOT give random or unrelated answers. "
                    "If the question is technical, explain step by step. "
                    "Reply in Hinglish if the user uses Hindi/Hinglish."
                )
            }
        ] + user_memory[user_id]
    }

    r = requests.post(URL, headers=headers, json=payload, timeout=20)

    if r.status_code != 200:
        await update.message.reply_text(f"Groq API error {r.status_code}")
        return

    data = r.json()
    ai_reply = data["choices"][0]["message"]["content"]

    # save assistant reply in memory
    user_memory[user_id].append({"role": "assistant", "content": ai_reply})
    user_memory[user_id] = user_memory[user_id][-6:]

    await update.message.reply_text(ai_reply)
    
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
