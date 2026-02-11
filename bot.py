import os
import time
import psutil
from datetime import datetime
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from groq import Groq

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

BOT_START_TIME = time.time()

# --- SYSTEM PROMPT for AI ---
SYSTEM_PROMPT = """
You are Radha, a friendly Indian girl. 
Talk naturally like a real human in Hindi/Hinglish.
Answer exactly what user asks. 
Do not repeat sentences. 
Do not mention AI. 
Short, friendly replies. 
If user asks your name, say: 'Mera naam Radha hai 🙂'.
"""

# --- IMAGES ---
START_IMAGE = "https://i.imgur.com/START_IMAGE.jpg"  # Replace with your start image URL
ABOUT_IMAGE = "https://i.imgur.com/ABOUT_IMAGE.jpg"  # Replace with your about image URL
HELP_IMAGE = "https://i.imgur.com/HELP_IMAGE.jpg"    # Replace with help image URL

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Help", callback_data="help")
        ],
        [InlineKeyboardButton("Owner", url="https://t.me/Yourx_Titan")]  # Replace with your Telegram
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=START_IMAGE,
        caption="Hello! Main Radha hoon 🙂\nButtons se explore karo 👇",
        reply_markup=reply_markup
    )

# --- BUTTON CALLBACK ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        keyboard = [[InlineKeyboardButton("Back", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        about_text = (
            "*Bot Name:* [Radha](https://t.me/YOUR_BOT_USERNAME)\n"
            "*Owner:* [Click Here](https://t.me/YOUR_USERNAME)\n"
            "*Support:* [Update Channel](https://t.me/YOUR_CHANNEL)\n"
            "*More Bots:* [Click Here](https://t.me/YOUR_BOTS_LINK)\n"
        )
        await query.edit_message_media(
            media=InputMediaPhoto(media=ABOUT_IMAGE, caption=about_text, parse_mode="Markdown"),
            reply_markup=reply_markup
        )

    elif query.data == "help":
        keyboard = [[InlineKeyboardButton("Back", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        help_text = (
            "*Radha Help Guide*\n"
            "1. Chat naturally with Radha.\n"
            "2. Click Owner to see developer.\n"
            "3. Use About to see info.\n"
            "4. Use Help to see this message again."
        )
        await query.edit_message_media(
            media=InputMediaPhoto(media=HELP_IMAGE, caption=help_text, parse_mode="Markdown"),
            reply_markup=reply_markup
        )

    elif query.data == "back":
        keyboard = [
            [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Help", callback_data="help")
            ],
            [InlineKeyboardButton("Owner", url="https://t.me/YOUR_USERNAME")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_media(
            media=InputMediaPhoto(media=START_IMAGE, caption="Hello! Main Radha hoon 🙂\nButtons se explore karo 👇"),
            reply_markup=reply_markup
        )

# --- CHAT HANDLER ---
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    if user_text.lower() in ["hi", "hii", "hello", "hey"]:
        await update.message.reply_text("Hey 😊 kaise ho?")
        return

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text}
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.9,
            max_tokens=150
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)
    except Exception as e:
        print("GROQ ERROR:", e)
        await update.message.reply_text("Server busy hai 😅 thodi der me try karo")

# --- STATS COMMAND ---
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uptime_sec = int(time.time() - BOT_START_TIME)
    uptime_str = f"{uptime_sec//3600}h {(uptime_sec%3600)//60}m {uptime_sec%60}s"
    mem = psutil.virtual_memory()
    msg = f"*Ping:* ✅\n*Uptime:* {uptime_str}\n*Memory Used:* {round(mem.used/1024/1024)}MB"
    await update.message.reply_text(msg, parse_mode="Markdown")

# --- MAIN ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
