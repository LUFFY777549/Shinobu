# Shinobu/Modules/tagall.py
from pyrogram import filters
from pyrogram.types import Message
from Shinobu import bot
from Shinobu.utils.admin import is_admin
import asyncio

@bot.on_message(filters.command(["tagall", "all"], prefixes=["/", ".", "!"]) & filters.group)
async def tag_all(client, message: Message):
    chat = message.chat
    user = message.from_user

    # ✅ Check if user is admin using our fixed utils
    if not await is_admin(client, chat.id, user.id):
        return await message.reply_text("❌ You must be an admin to use this command!")

    # Custom message
    text = message.text.split(maxsplit=1)
    custom_msg = text[1] if len(text) > 1 else "⚡ Attention everyone!"

    status_msg = await message.reply_text("🔁 Tagging all members, please wait...")

    members = client.get_chat_members(chat.id)
    batch = []
    count = 0

    async for m in members:
        if m.user.is_bot:
            continue
        mention = m.user.mention
        batch.append(mention)
        count += 1

        if len(batch) == 5:
            msg = f"{custom_msg}\n\n" + " ".join(batch)
            try:
                await client.send_message(chat.id, msg)
            except Exception:
                pass
            await asyncio.sleep(2)
            batch.clear()

    if batch:
        msg = f"{custom_msg}\n\n" + " ".join(batch)
        await client.send_message(chat.id, msg)

    await status_msg.edit_text(f"✅ Successfully tagged {count} members!")