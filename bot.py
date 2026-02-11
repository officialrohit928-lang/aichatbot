import os
import requests
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BOT_USERNAME = "RadhaSharma_bot"
OWNER_USERNAME = "YOURX_TITAN"

START_IMAGE = "https://files.catbox.moe/h8wo87.jpg"
HELP_IMAGE  = "https://files.catbox.moe/h8wo87.jpg"
ABOUT_IMAGE = "https://files.catbox.moe/2ghxh0.jpg"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ================= AI PERSONALITY =================
SYSTEM_PROMPT = """
You are Radha.

Personality:
- Friendly, sweet, human-like
- Hinglish / Hindi tone
- Short replies
- Emotion samajh ke jawab do
- Kabhi AI jaisa explain mat karo

Rules:
- If asked "tum kaun ho?" reply only: "Main Radha hoon 😊"
- No technical talk
- No long lectures
"""

# ================= AI FUNCTION =================
def ask_groq(text: str) -> str:
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.9,
        "max_tokens": 120
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=20)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except:
        return "Thoda issue aa gaya 😕 baad me baat karte hain"

# ================= /START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = (
        "❖ HEY I'M **Radha 🐵**\n\n"
        "⟡ An AI based chat-bot.\n\n"
        "» Chat like human (DM + Group) 😘\n"
        "» No abuse, no ads, zero downtime.\n"
        "» Powerful & useful features.\n\n"
        "➜ Click **HELP** to see all commands."
    )

    keyboard = [
        [InlineKeyboardButton("➕ ADD ME IN YOUR GROUP ➕",
         url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("OWNER", callback_data="owner"),
            InlineKeyboardButton("ABOUT", callback_data="about")
        ],
        [InlineKeyboardButton("HELP & COMMANDS", callback_data="help")]
    ]

    await update.message.reply_photo(
        photo=START_IMAGE,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= BUTTON HANDLER =================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # HELP PAGE
    if query.data == "help":
        caption = (
            "❖ **CHOOSE CATEGORY FOR HELP**\n\n"
            "» If any issue comes – SUPPORT CHAT"
        )

        keyboard = [
            [
                InlineKeyboardButton("BASIC", callback_data="basic"),
                InlineKeyboardButton("CHAT-BOT", callback_data="chatbot")
            ],
            [
                InlineKeyboardButton("INFO", callback_data="info"),
                InlineKeyboardButton("TAGS", callback_data="tags")
            ],
            [
                InlineKeyboardButton("RANK", callback_data="rank"),
                InlineKeyboardButton("WELCOME", callback_data="welcome")
            ],
            [InlineKeyboardButton("⬅ BACK", callback_data="back")]
        ]

        await query.message.edit_media(
            media={
                "type": "photo",
                "media": HELP_IMAGE,
                "caption": caption,
                "parse_mode": "Markdown"
            },
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ABOUT PAGE
    elif query.data == "about":
        caption = (
            f"❖ [**Radha 🐵**](https://t.me/{RadhaSharma_bot}) — AN AI BASED CHAT-BOT\n"
            "CHAT LIKE HUMAN (DM + GROUP) 😘\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "• **WRITTEN IN** » PYTHON\n"
            "• **DATABASE** » MONGO-DB\n"
            "• **HELP WITH** » PYROGRAM\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "➤ NO ABUSE, NO ADS, ZERO DOWNTIME.\n"
            "➤ PROMOTE ME ADMIN WITH BASIC RIGHTS.\n"
            "➤ ADD ME NOW IN YOUR GROUPS.\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "◆ UPDATES CHANNEL ➜ [SHADOW](https://t.me/Yourx_shadow)\n"
            "◆ SUPPORT CHAT ➜ [Radha Support](https://t.me/+RHx822f_tV0wZTZl)\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "➤ [BOT STATUS & MORE BOTS](https://t.me/Yourx_shadow)\n"
            f"➤ [PAID PROMOTION – CONTACT HERE](https://t.me/{OWNER_USERNAME})"
        )

        keyboard = [
            [
                InlineKeyboardButton("SUPPORT", url="https://t.me/Purvi_Updates"),
                InlineKeyboardButton("UPDATE", url="https://t.me/Purvi_Bots")
            ],
            [InlineKeyboardButton("⬅ BACK", callback_data="back")]
        ]

        await query.message.edit_media(
            media={
                "type": "photo",
                "media": ABOUT_IMAGE,
                "caption": caption,
                "parse_mode": "Markdown"
            },
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # OWNER
    elif query.data == "owner":
        await query.message.reply_text(f"Owner 👑 → https://t.me/{OWNER_USERNAME}")

    # BACK
    elif query.data == "back":
        await start(query.message, context)

# ================= CHAT =================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text in ["tum kon ho", "tum kaun ho", "who are you"]:
        await update.message.reply_text("Main Radha hoon 😊")
        return

    reply = ask_groq(update.message.text)
    await update.message.reply_text(reply)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Purvi bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
