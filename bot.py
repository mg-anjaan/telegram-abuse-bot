import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from group_guard_bot import setup_group_guard

BOT_TOKEN = "8383391764:AAFm0-a1tYbrwGdRwoKLzTqPVz48xH_mNC4"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("✅ Bot is live and secured with Group Guard!")

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("🤖 Available commands:\n/start - Check bot status\n/help - Help info")

setup_group_guard(dp)

async def handle(request):
    return web.Response(text="Bot running fine ✅")

app = web.Application()
app.router.add_get("/", handle)

async def run_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))