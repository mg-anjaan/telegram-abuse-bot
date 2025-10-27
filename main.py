import asyncio
from bot import bot, dp

async def main():
    print("🤖 Starting bot locally with polling mode...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
