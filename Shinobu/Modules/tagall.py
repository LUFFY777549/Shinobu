# Shinobu/Modules/tagall.py
from pyrogram import filters
from pyrogram.types import Message
from Shinobu import bot
from Shinobu.utils.admin import is_admin
import asyncio

# Active tagging chats list
spam_chats = set()


# ---------------- TAG ALL ---------------- #
@bot.on_message(filters.command(["tagall", "all"], prefixes=["/", ".", "!"]) & filters.group)
async def tag_all(client, message: Message):
    chat_id = message.chat.id
    user = message.from_user

    # Only admins
    if not await is_admin(client, chat_id, user.id):
        return await message.reply_text("❌ Only admins can mention all!")

    # Get custom text or replied message
    if len(message.command) > 1 and message.reply_to_message:
        return await message.reply_text("❌ Give only one argument (text OR reply), not both!")
    elif len(message.command) > 1:
        mode = "text_on_cmd"
        msg = " ".join(message.command[1:])
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
    else:
        return await message.reply_text("⚠️ Reply to a message or add text to mention all users!")

    # Add to spam list
    spam_chats.add(chat_id)
    await message.reply_text("🔁 Starting mass mention... use /cancel to stop.")

    user_count = 0
    mention_text = ""

    async for member in client.get_chat_members(chat_id):
        if chat_id not in spam_chats:
            break
        if member.user.is_bot:
            continue

        user_count += 1
        mention_text += f"[{member.user.first_name}](tg://user?id={member.user.id}), "

        if user_count % 5 == 0:
            try:
                if mode == "text_on_cmd":
                    text = f"{msg}\n\n{mention_text}"
                    await client.send_message(chat_id, text)
                else:
                    await msg.reply_text(mention_text)
            except Exception:
                pass
            await asyncio.sleep(2)
            mention_text = ""

    # Send leftover mentions
    if mention_text:
        try:
            if mode == "text_on_cmd":
                await client.send_message(chat_id, f"{msg}\n\n{mention_text}")
            else:
                await msg.reply_text(mention_text)
        except Exception:
            pass

    try:
        spam_chats.remove(chat_id)
    except:
        pass

    await message.reply_text("✅ Done tagging all members!")


# ---------------- CANCEL TAGGING ---------------- #
@bot.on_message(filters.command("cancel") & filters.group)
async def cancel_tagging(client, message: Message):
    chat_id = message.chat.id
    user = message.from_user

    if chat_id not in spam_chats:
        return await message.reply_text("❌ No tagging process is running!")

    if not await is_admin(client, chat_id, user.id):
        return await message.reply_text("❌ Only admins can cancel tagging!")

    try:
        spam_chats.remove(chat_id)
    except:
        pass
    await message.reply_text("🛑 Tagging stopped successfully!")