# Shinobu/Modules/upscale.py
from io import BytesIO
from pyrogram import filters
from pyrogram.types import Message
from PIL import Image
from Shinobu import bot  # Your Pyrogram client

# Scale factor
SCALE = 2  # 2x upscale

@bot.on_message(filters.command("up") & filters.reply & (filters.private | filters.group))
async def upscale_image(client, message: Message):
    if not message.reply_to_message.photo:
        return await message.reply("❌ Please reply to a photo to upscale it.")

    status_msg = await message.reply("🔄 Upscaling your image locally, please wait...")

    try:
        # Download the photo
        file_path = await message.reply_to_message.download()
        img = Image.open(file_path)

        # Get new size
        new_size = (img.width * SCALE, img.height * SCALE)

        # Upscale using PIL (bicubic)
        upscaled = img.resize(new_size, Image.BICUBIC)

        # Save to buffer
        buf = BytesIO()
        upscaled.save(buf, format="JPEG")
        buf.seek(0)

        # Send upscaled image
        await status_msg.edit_text("✅ ɪᴍᴀɢᴇ ᴜᴘꜱᴄᴀʟᴇᴅ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ")
        await message.reply_photo(buf, caption=f"Here is your {SCALE}x upscaled image!")

    except Exception as e:
        await status_msg.edit_text(f"❌ Upscale failed.\nError: `{e}`")