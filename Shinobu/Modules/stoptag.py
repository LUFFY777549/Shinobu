# ========================= STOP TAG ========================= #

import logging
from pyrogram import filters
from Shinobu import bot
from Shinobu.db import stop_tag, is_tagging_active
from Shinobu.utils import is_user_admin

logger = logging.getLogger(__name__)

@bot.on_message(filters.command("stoptag") & filters.group)
async def stop_tag_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_user_admin(client, chat_id, user_id):
        logger.info(f"Non-admin {user_id} tried /stoptag in {chat_id}")
        return await message.reply_text("❌ Only admins can stop tagging!")

    if await is_tagging_active(chat_id):
        await stop_tag(chat_id)
        await message.reply_text("🛑 Tagging stopped successfully.")
    else:
        await message.reply_text("⚠️ No ongoing tagging process.")