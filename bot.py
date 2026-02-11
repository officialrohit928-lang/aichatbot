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

    # sirf last 2 messages ka context
    user_memory[user_id] = [{"role": "user", "content": user_text}]

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
    "Your name is Baka. "
    "Whenever someone asks 'tum kon ho' or similar, reply ONLY: 'Main Baka hoon 😊'. "
    "Do NOT explain that you are an AI. "
    "Do NOT change topic. "
    "Do NOT give extra information. "
    "Talk in short, simple, friendly Hinglish. "
    "Reply like a normal person in casual chat. "
    "Examples:\n"
    "User: Kaise ho\nAssistant: Mast hoon 😊\n"
    "User: Btao kon ho\nAssistant: Main Baka hoon 😊\n"
    "User: Mast ek dam\nAssistant: Sahi hai 😄"
           )
         }
       }
    r = requests.post(URL, headers=headers, json=payload, timeout=20)

    if r.status_code != 200:
        await update.message.reply_text("Thoda issue aa raha hai 😅 baad me try karo")
        return

    data = r.json()
    reply_text = data["choices"][0]["message"]["content"]

    await update.message.reply_text(reply_text)
    
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
