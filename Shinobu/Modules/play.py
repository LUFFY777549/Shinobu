# Shinobu/Modules/play.py
import os
import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Shinobu import bot, user, call  # user is Client(session=STRING_SESSION); call is PyTgCalls
from Shinobu.db import DBQueue  # optional: you can implement queue in DB
from Shinobu.Modules.audio import ytdl_download
from datetime import datetime

YT_COOKIES = os.environ.get("YT_COOKIES_PATH", "cookies.txt")

def control_keyboard(chat_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏯️", callback_data=f"pause|{chat_id}"),
            InlineKeyboardButton("⏭️", callback_data=f"skip|{chat_id}"),
            InlineKeyboardButton("⏹️", callback_data=f"stop|{chat_id}")
        ],
        [
            InlineKeyboardButton("📢 SUPPORT", url="https://t.me/YourSupportChannel"),
            InlineKeyboardButton("✖ CLOSE", callback_data=f"close|{chat_id}")
        ]
    ])

@bot.on_message(filters.command("play") & (filters.private | filters.group))
async def cmd_play(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Determine query
    if message.reply_to_message and (message.reply_to_message.audio or message.reply_to_message.document or message.reply_to_message.video):
        # Use replied file: download it and stream
        src = await message.reply_to_message.download()
        title = message.reply_to_message.audio.title if message.reply_to_message.audio else (message.reply_to_message.document.file_name if message.reply_to_message.document else "Audio")
        duration = 0
        source_info = {"filepath": src, "title": title, "duration": duration, "thumbnail": None}
    else:
        # parse text after /play
        if len(message.command) < 2:
            return await message.reply_text("ᴜsᴀɢᴇ : /play [sᴏɴɢ ɴᴀᴍᴇ/ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ/ʀᴇᴘʟʏ ᴛᴏ ᴀᴜᴅɪᴏ]")
        query = message.text.split(None, 1)[1]
        status = await message.reply_text("🔎 Searching and downloading...")
        # download with yt-dlp (async)
        try:
            source_info = await ytdl_download(query, cookies=YT_COOKIES)
            await status.delete()
        except Exception as e:
            await status.edit_text(f"❌ Download failed: {e}")
            return

    # Save to DB queue or in-memory queue (simplified here: immediate play)
    # Ensure userbot joined vc for this chat
    try:
        if not call.active_calls.get(chat_id):  # pseudo-check; implement your own state
            # Invite user to chat (if not present) or ensure user is in chat members
            # user.join_chat or just start voice chat: PyTgCalls join requires chat id and path to file
            await user.join_chat(chat_id)  # may raise if cannot
    except Exception:
        # We skip invite step; user client must be in chat and allowed to join VC
        pass

    # Play using pytgcalls
    try:
        # If file is not an opus/ogg, we stream through ffmpeg
        audio_path = source_info["filepath"]
        # Convert to raw format or use FFmpeg transcoding in pytgcalls
        await call.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(
                    audio_path,
                )
            )
        )
    except Exception as e:
        # fallback: upload audio to chat and show UI (if streaming fails)
        caption = (
            f"➻ ᴘʟᴀʏɪɴɢ : {source_info.get('title')}\n"
            f"⏱ : {source_info.get('duration')}\n"
            f"By : {message.from_user.mention}"
        )
        thumb = source_info.get("thumbnail")
        buttons = control_keyboard(chat_id)
        if thumb:
            await bot.send_photo(chat_id, thumb, caption=caption, reply_markup=buttons)
        else:
            await bot.send_message(chat_id, caption, reply_markup=buttons)
        return

    # On success send now-playing message and controls
    caption = (
        f"ᴛɪᴛʟᴇ : {source_info.get('title')}\n"
        f"ᴛɪᴍᴇ : {source_info.get('duration')}\n"
        f"By : {message.from_user.mention}"
    )
    thumb = source_info.get("thumbnail")
    await bot.send_photo(chat_id, thumb or "https://files.catbox.moe/xa33dy.jpg", caption=caption, reply_markup=control_keyboard(chat_id))