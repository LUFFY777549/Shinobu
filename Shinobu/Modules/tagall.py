# Shinobu/Modules/tagall.py
from pyrogram import filters
from pyrogram.types import Message
from Shinobu import bot
import asyncio

# ---------------- TagAll Command ---------------- #
@bot.on_message(filters.command(["tagall", "all"], prefixes=["/", ".", "!"]) & filters.group)
async def tag_all(client, message: Message):
    user = message.from_user
    chat = message.chat

    # Optional message text
    text = message.text.split(maxsplit=1)
    custom_msg = text[1] if len(text) > 1 else "Attention everyone!"

    # Check admin rights
    member = await client.get_chat_member(chat.id, user.id)
    if member.status not in ("administrator", "creator"):
        return await message.reply_text("❌ Only admins can use this command!")

    await message.reply_text("🔁 Tagging all members, please wait...")

    members = client.get_chat_members(chat.id)
    batch = []
    count = 0
    async for m in members:
        if m.user.is_bot:
            continue
        mention = m.user.mention
        batch.append(mention)
        count += 1

        # Send in batches of 5 mentions
        if len(batch) == 5:
            msg = f"{custom_msg}\n\n" + " ".join(batch)
            try:
                await message.reply_text(msg)
            except Exception:
                pass
            await asyncio.sleep(2)
            batch.clear()

    # If any remaining
    if batch:
        msg = f"{custom_msg}\n\n" + " ".join(batch)
        await message.reply_text(msg)

    await message.reply_text(f"✅ Tagged {count} members successfully!")