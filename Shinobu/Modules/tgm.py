# Shinobu/Modules/tgm.py
import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from Shinobu import bot  # Your Pyrogram client

CATBOX_UPLOAD_URL = "https://catbox.moe/user/api.php"
CATBOX_API_KEY = "YOUR_CATBOX_API_KEY"  # Optional, lekin faster uploads ke liye

@bot.on_message(filters.command("tgm") & filters.reply & (filters.private | filters.group))
async def tgm_upload(client, message: Message):
    replied = message.reply_to_message

    if not replied.photo and not (replied.document and replied.document.mime_type.startswith("image")):
        return await message.reply("❌ Please reply to an image/photo to generate link.")

    status_msg = await message.reply("🔄 Uploading your image, please wait...")

    try:
        file_path = await replied.download()
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field("reqtype", "fileupload")
            data.add_field("fileToUpload", open(file_path, "rb"))
            if CATBOX_API_KEY:
                data.add_field("userhash", CATBOX_API_KEY)

            async with session.post(CATBOX_UPLOAD_URL, data=data) as resp:
                link = await resp.text()

        await status_msg.edit_text(f"✅ Yᴏᴜʀ ʟɪɴᴋ sᴜᴄᴄessғᴜʟ Gᴇɴ: {link}")

    except Exception as e:
        await status_msg.edit_text(f"❌ Upload failed.\nError: `{e}`")