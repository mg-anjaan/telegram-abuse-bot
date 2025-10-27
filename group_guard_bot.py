from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your real bot token
ADMIN_ID = 7996780813  # Replace with your Telegram ID

BAD_WORDS = [
    "bhosdike", "madarchod", "chod", "lund", "randi", "mc", "bc", "chutiya", "fucker", "fuck",
    "bsdk", "gaand", "kutte", "harami", "kamina", "rakhail", "suar", "chud", "gandu",
    "tatti", "kutiya", "betichod", "behenchod", "loda", "chodna", "lauda",
    "chut", "bc", "mc", "gand", "lodu", "bhenkelode", "madarchkd", "randi", "chutiyta"
]

LINK_KEYWORDS = ["t.me", "http", "https", "telegram.me", "bit.ly"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot active: abusive users will be muted, and link messages deleted!"
    )

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()
    user = message.from_user

    # Abusive message detection
    if any(word in text for word in BAD_WORDS):
        try:
            await message.chat.restrict_member(
                user.id,
                ChatPermissions(can_send_messages=False)
            )
            await message.reply_text(
                f"🚫 @{user.username or user.first_name} has been permanently muted for abusive language."
            )
            await context.bot.send_message(
                ADMIN_ID,
                f"⚠️ User muted:\n👤 {user.full_name}\n🆔 ID: {user.id}\n🗨️ Message: {message.text}"
            )
        except Exception as e:
            await message.reply_text(f"⚠️ Could not mute user: {e}")
        return

    # Link detection in message text
    if any(link in text for link in LINK_KEYWORDS):
        try:
            await message.delete()
            await message.chat.send_message(
                f"⚠️ @{user.username or user.first_name}, posting links is not allowed!"
            )
            await context.bot.send_message(
                ADMIN_ID,
                f"🔗 Link message deleted:\n👤 {user.full_name}\n🆔 ID: {user.id}\n🗨️ Message: {message.text}"
            )
        except Exception as e:
            print("Error deleting link message:", e)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    app.run_polling()

if __name__ == "__main__":
    main()
