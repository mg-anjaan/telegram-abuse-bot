from aiogram import types

def setup_group_guard(dp):
    @dp.message()
    async def group_protection(message: types.Message):
        # Work only in groups
        if message.chat.type not in ["group", "supergroup"]:
            return

        # --- BLOCK TELEGRAM LINKS (only for members, not admins) ---
        if message.text and ("t.me/" in message.text or "telegram.me/" in message.text):
            member = await message.chat.get_member(message.from_user.id)
            if not (member.is_chat_admin() or member.is_chat_creator()):
                await message.delete()
                await message.answer(f"🚫 {message.from_user.first_name}, link sharing is not allowed here!")
            return

        # --- ABUSIVE / SPAM WORD FILTER (ENGLISH + HINDI + SLANG) ---
        banned_words = [
            # English abusive
            "fuck", "bitch", "shit", "asshole", "bastard", "slut", "jerk", "dumb",
            "idiot", "stupid", "loser", "moron",

            # Hindi (Romanized)
            "madarchod", "behenchod", "bhenchod", "chutiya", "chutiye",
            "gaand", "gandu", "gaandu", "bhosdike", "bhosi", "randi", "kamina",
            "harami", "kutta", "kuttiya", "lund", "lavda", "laude", "lode",
            "saala", "gadwa", "bur", "bc", "mc", "chut", "maa ka", "behen ka",
            "teri maa", "teri behen", "bhosri", "bhosriwale", "rakhail", "bkl",
            "chakka", "hijra", "launde", "rand", "gaandmasti", "kutte",

            # Hindi (Devanagari)
            "मादरचोद", "भेंचोद", "चूतिया", "गांडू", "गांड", "हरामी",
            "रांडी", "लंड", "लवड़ा", "साला", "कुत्ता", "कुत्ती", "गदवा",
            "भोसड़ीके", "भोसड़ी", "बुर", "चूत", "माँ के", "बहन के", "कमिना",
            "हिजड़ा", "लौड़ा", "लवड़ा", "कमीना"
        ]

        # Check for abusive word
        if message.text and any(word.lower() in message.text.lower() for word in banned_words):
            await message.delete()

            try:
                # Permanently restrict user (mute)
                await message.bot.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id,
                    permissions=types.ChatPermissions(can_send_messages=False)
                )
                await message.answer(
                    f"🚷 {message.from_user.first_name} has been permanently muted for using abusive or offensive language!"
                )
            except Exception as e:
                await message.answer(
                    f"⚠️ Tried to mute {message.from_user.first_name}, but I may not have admin rights.\n({e})"
                )
            return

    # --- WELCOME NEW MEMBER ---
    @dp.chat_member()
    async def greet_new_member(event: types.ChatMemberUpdated):
        if event.new_chat_member.status == "member":
            await event.bot.send_message(
                event.chat.id,
                f"👋 Welcome {event.new_chat_member.user.first_name} to {event.chat.title}!"
            )
