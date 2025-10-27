import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from group_guard_bot import setup_group_guard

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("✅ Bot is live and working!")

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("🤖 Available commands:\n/start - Check if bot is live\n/help - Show help info")

setup_group_guard(dp)

WEBHOOK_URL = "https://telegram-abuse-bot.onrender.com/webhook"

async def handle(request):
    return web.Response(text="Bot is running fine ✅")

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(app):
    await bot.delete_webhook()
    print("Webhook deleted.")

app = web.Application()
app.router.add_get("/", handle)

async def webhook_handler(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()

app.router.add_post("/webhook", webhook_handler)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
