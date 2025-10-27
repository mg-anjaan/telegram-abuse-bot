import os
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7996780813

BAD_WORDS = [
    "bhosdike", "madarchod", "chod", "lund", "randi", "mc", "bc", "chutiya",
    "fucker", "fuck", "bsdk", "gaand", "kutte", "harami", "kamina", "rakhail",
    "suar", "chud", "gandu", "tatti", "kutiya", "betichod", "behenchod",
    "loda", "chodna", "lauda", "chut", "bc", "mc", "gand", "lodu", "bhenkelode",
    "madarchkd", "randi", "chutiyta"
]

LINK_KEYWORDS = ["t.me", "http", "https", "telegram.me", "bit.ly"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot active! Abusive users will be muted, and link messages deleted automatically."
    )

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()
    user = message.from_user

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
        return

    if user and user.bio:
        bio_text = user.bio.lower()
        if any(link in bio_text for link in LINK_KEYWORDS):
            try:
                await message.delete()
                await message.chat.send_message(
                    f"⚠️ @{user.username or user.first_name}, your bio contains a link. Remove it to continue!"
                )
                await context.bot.send_message(
                    ADMIN_ID,
                    f"🚨 Bio link detected:\n👤 {user.full_name}\n🆔 ID: {user.id}\n📝 Bio: {user.bio}"
                )
            except Exception as e:
                print("Error deleting bio link message:", e)

async def handle(request):
    return web.Response(text="Bot is running ✅")

def start_webserver():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    web.run_app(app, port=int(os.environ.get("PORT", 8080)))

def main():
    import threading
    threading.Thread(target=start_webserver, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    print("✅ Bot started successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()
