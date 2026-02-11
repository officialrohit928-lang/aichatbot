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
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    if user_text.lower() in ["hi", "hii", "hello", "hey"]:
        await update.message.reply_text("Hey 😊 kaise ho?")
        return

    messages = [
        {
            "role": "system",
            "content": (
                "You are Radha, a sweet Indian girl. "
                "You reply like a real human, not an AI. "
                "You answer exactly what the user asks. "
                "Replies should be short, natural and friendly."
            )
        },
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
        await update.message.reply_text("Server thoda busy hai 😅 thodi der me try karo")
# ================== BUTTONS ==================
def start_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ADD ME IN YOUR GROUP ➕",
         url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("TITAN", url=f"https://t.me/{OWNER_USERNAME}"),
            InlineKeyboardButton("ABOUT", callback_data="about")
        ]
    ])

def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 BACK", callback_data="back")]
    ])

# ================== HANDLERS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        START_TEXT,
        reply_markup=start_buttons(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # ABOUT
    if query.data == "about":
        await query.edit_message_text(
            ABOUT_TEXT,
            reply_markup=back_button(),
            parse_mode="Markdown"
        )

    # BACK
    elif query.data == "back":
        await query.edit_message_text(
            START_TEXT,
            reply_markup=start_buttons(),
            parse_mode="Markdown"
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
