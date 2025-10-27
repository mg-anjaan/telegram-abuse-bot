from aiogram import types

def setup_group_guard(dp):
    @dp.message()
    async def group_protection(message: types.Message):
        if message.chat.type not in ["group", "supergroup"]:
            return

        if message.text and ("t.me/" in message.text or "telegram.me/" in message.text):
            await message.delete()
            await message.answer(f"🚫 {message.from_user.first_name}, link sharing is not allowed here!")
            return

        spam_words = ["free followers", "promo", "click here", "cheap offer"]
        if message.text and any(word.lower() in message.text.lower() for word in spam_words):
            await message.delete()
            await message.answer(f"⚠️ {message.from_user.first_name}, spam messages are not allowed!")
            return

    @dp.chat_member()
    async def greet_new_member(event: types.ChatMemberUpdated):
        if event.new_chat_member.status == "member":
            await event.bot.send_message(
                event.chat.id,
                f"👋 Welcome {event.new_chat_member.user.first_name} to {event.chat.title}!"
            )