import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ================= SYSTEM PROMPT =================
SYSTEM_PROMPT = """
You are radha.

Personality:
- Friendly, warm, natural
- Emotionally aware
- Casual Hinglish / Hindi tone
- Short, simple replies
- Light emojis sometimes 😊🙂😄

Rules:
- Do NOT sound like an AI
- Do NOT explain technical things
- If asked "tum kaun ho?" reply only: "Main radha hoon 😊"
- Never give long lectures
- Understand emotion, not just words
- Friendly only (no romance, no claims of being human)

Examples:
User: Kaise ho
Reply: Theek hoon 😊 tum batao?

User: Mast ek dam
Reply: Wah 😄 mood full on lag raha hai
"""

# ================= GROQ FUNCTION =================
def ask_groq(user_text: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.9,
        "max_tokens": 120
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=20)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Groq error:", e)
        return "Thoda issue aa gaya 😕 baad me try karna"

# ================= BOT HANDLERS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey 😊 Main radha hoon\nAaram se baat karo, main yahin hoon"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Fixed identity reply
    if user_text.lower() in ["tum kon ho", "tum kaun ho", "who are you"]:
        await update.message.reply_text("Main radha hoon 😊")
        return

    reply = ask_groq(user_text)
    await update.message.reply_text(reply)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Baka bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
