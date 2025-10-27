# Shinobu/Modules/tagall.py
import asyncio
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode
from Shinobu import bot
from Shinobu.utils.admin import is_user_admin
from Shinobu.db.tagging import start_tag, stop_tag, is_tagging_active

# -------------------- EMOJIS -------------------- #
EMOJIS = ["🦁", "🐯", "🐱", "🐶", "🐺", "🐻", "🐼", "🐹", "🐭", "🐰", "🦊", "🐮", "🐷"]

# Temporary storage for tag text
TAG_TEXT = {}


# -------------------- TAGALL COMMAND -------------------- #
@bot.on_message(filters.command("tagall") & filters.group)
async def tagall(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # ✅ Admin check
    if not await is_admin(client, chat_id, user_id):
        return await message.reply_text("❌ Only admins can use this command!")

    # ✅ If reply → use that text
    if message.reply_to_message:
        tag_text = message.reply_to_message.text or ""
        reply_to_id = message.reply_to_message.id
    else:
        tag_text = " ".join(message.command[1:]) or ""
        reply_to_id = None

    TAG_TEXT[chat_id] = {"text": tag_text, "reply_id": reply_to_id}

    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Send", callback_data="send_tag"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_tag"),
            ]
        ]
    )

    preview = " ".join(random.choices(EMOJIS, k=10))
    await message.reply_text(
        f"{tag_text}\n\n<b>Preview:</b>\n{preview}",
        reply_markup=markup,
        reply_to_message_id=reply_to_id if reply_to_id else None,
        parse_mode=ParseMode.HTML,
    )


# -------------------- BUTTON HANDLER -------------------- #
@bot.on_callback_query(filters.regex("^(send_tag|cancel_tag)$"))
async def handle_buttons(client, cq):
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id
    data = cq.data

    # Cancel button
    if data == "cancel_tag":
        return await cq.edit_message_text("❌ Tagging cancelled.")

    # Send button
    if data == "send_tag":
        await cq.edit_message_text("🚀 Tagging started...")
        await start_tag(chat_id, user_id)

        # Counters
        success_count, bot_count, deleted_count, fail_count = 0, 0, 0, 0
        members = []

        # Collect members
        async for m in client.get_chat_members(chat_id):
            if m.user.is_bot:
                bot_count += 1
                continue
            if m.user.is_deleted:
                deleted_count += 1
                continue
            members.append(m.user)

        if not members:
            await stop_tag(chat_id)
            return await cq.edit_message_text("⚠️ No valid members found!")

        # Get saved text and reply target
        tag_info = TAG_TEXT.get(chat_id, {"text": "", "reply_id": None})
        text = tag_info["text"]
        reply_to_id = tag_info["reply_id"]

        chunk_size = 10
        for i in range(0, len(members), chunk_size):
            if not await is_tagging_active(chat_id):
                await client.send_message(chat_id, "🛑 Tagging stopped manually.")
                return

            chunk = members[i : i + chunk_size]
            mentions = " ".join(
                [f"[{random.choice(EMOJIS)}](tg://user?id={m.id})" for m in chunk]
            )

            msg = f"{text}\n\n{mentions}" if text else mentions

            try:
                await client.send_message(
                    chat_id,
                    msg.strip(),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_to_message_id=reply_to_id if reply_to_id else None,
                )
                success_count += len(chunk)
            except Exception:
                fail_count += len(chunk)

            await asyncio.sleep(3)

        await stop_tag(chat_id)
        await client.send_message(
            chat_id,
            (
                f"✅ Tagging completed!\n\n"
                f"👤 Successful: `{success_count}`\n"
                f"🤖 Bots skipped: `{bot_count}`\n"
                f"🗑 Deleted accounts: `{deleted_count}`\n"
                f"⚠️ Failed: `{fail_count}`\n\n"
                f"💬 Started by: [{cq.from_user.first_name}](tg://user?id={user_id})"
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=reply_to_id if reply_to_id else None,
        )