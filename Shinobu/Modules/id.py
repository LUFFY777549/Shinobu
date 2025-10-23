# id.py
from pyrogram import filters
from Shinobu import bot

@bot.on_message(filters.command("id") & (filters.private | filters.group))
async def get_id(client, message):
    user = message.from_user
    chat = message.chat

    msg_id = message.message_id
    user_id = user.id
    chat_id = chat.id

    text = (
        f"ᴍᴇssᴀɢᴇ ɪᴅ: {msg_id}\n"
        f"ʏᴏᴜʀ ɪᴅ: {user_id}\n"
        f"ᴄʜᴀᴛ ɪᴅ: {chat_id}"
    )

    # Agar reply hai to replied user ka info bhi add karein
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        replied_msg_id = message.reply_to_message.message_id
        text += (
            f"\n\nʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ: {replied_msg_id}\n"
            f"ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ: {replied_user.id}"
        )

    await message.reply_text(text)