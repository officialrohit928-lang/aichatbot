import os
from telegram.ext import filters
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler
)

# ================== CONFIG ==================
BOT_TOKEN = "8168458901:AAHYY3r_B37PdUBdyABaFw7njJKWjFfBzno"
# Start Image URL
START_IMAGE = "https://files.catbox.moe/h8wo87.jpg"  # Replace with your start image link
ABOUT_IMAGE = "https://files.catbox.moe/2ghxh0.jpg"  # Replace with your about image link

import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BOT_USERNAME = "RadhaSharma_bot"     # without @
OWNER_USERNAME = "Yourx_Titan"      # without @

UPDATE_CHANNEL = "https://t.me/Yourx_shadow"
SUPPORT_CHAT = "https://t.me/+RHx822f_tV0wZTZl"
MORE_BOTS = "https://t.me/Yourx_shadow"
PAID_PROMO = f"https://t.me/{OWNER_USERNAME}"


# ================== TEXT ==================
START_TEXT = (
    "❖ HEY I'M **Radha 🐵**\n\n"
    "⟡ An AI based chat-bot.\n\n"
    "» Chat like human (DM + Group) 😘\n"
    "» No abuse, no ads, zero downtime.\n"
    "» Powerful & useful features.\n\n"
    "➜ Use buttons below ⬇"
)

ABOUT_TEXT = (
    f"❖ [**Radha 🐵**](https://t.me/{BOT_USERNAME}) — AN AI BASED CHAT-BOT\n"
    "CHAT LIKE HUMAN (DM + GROUP) 😘\n\n"
    "━━━━━━━━━━━━━━\n\n"
    "• **WRITTEN IN** » PYTHON\n"
    "• **DATABASE** » MONGO-DB\n"
    "• **HELP WITH** » PYROGRAM\n\n"
    "━━━━━━━━━━━━━━\n\n"
    "◆ UPDATES CHANNEL ➜ [SHADOW](" + UPDATE_CHANNEL + ")\n"
    "◆ SUPPORT CHAT ➜ [Radha support](" + SUPPORT_CHAT + ")\n\n"
    "━━━━━━━━━━━━━━\n\n"
    "➤ [BOT STATUS & MORE BOTS](" + MORE_BOTS + ")\n"
    "➤ [PAID PROMOTION](" + PAID_PROMO + ")"
)

SYSTEM_PROMPT = """
Tum ek friendly Indian girl ho.
Tumhara naam Radha hai.

Rules:
- Jo pucha jaye uska direct answer do
- Repeated reply mat dena
- Short, natural Hinglish me baat karo
- Human emotions samjho
- Over explain mat karo
- AI ya bot hone ka mention mat karo
- Agar koi naam puche to bolo: "Mera naam Radha hai 😊"
- Greeting pe friendly reply do
"""
# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("About", callback_data="about")],
        [InlineKeyboardButton("Owner", url="https://t.me/YOUR_USERNAME")]  # Replace with your Telegram
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(
        photo=START_IMAGE,
        caption="Hello! Main Radha hoon 🙂\nButtons se explore karo 👇",
        reply_markup=reply_markup
    )

# About Button Callback
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "about":
        keyboard = [[InlineKeyboardButton("Back", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        about_text = (
            "Bot Name: Radha 🤖\n"
            "Owner: [Click Here](https://t.me/YOUR_USERNAME)\n"
            "Support: [Update Channel](https://t.me/YOUR_CHANNEL)\n"
            "More Bots: [Click Here](https://t.me/YOUR_BOTS_LINK)\n"
        )
        
        await query.edit_message_media(
            media=InputMediaPhoto(media=ABOUT_IMAGE, caption=about_text, parse_mode="Markdown"),
            reply_markup=reply_markup
        )
    
    elif query.data == "back":
        # recreate start keyboard
        keyboard = [
            [InlineKeyboardButton("About", callback_data="about")],
            [InlineKeyboardButton("Owner", url="https://t.me/YOUR_USERNAME")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_media(
            media=InputMediaPhoto(media=START_IMAGE, caption="Hello! Main Radha hoon 🙂\nButtons se explore karo 👇"),
            reply_markup=reply_markup
        )

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
