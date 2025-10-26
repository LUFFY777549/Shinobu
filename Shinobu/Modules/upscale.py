# Shinobu/Modules/upscale.py
from io import BytesIO
from pyrogram import filters
from pyrogram.types import Message
from PIL import Image
from Shinobu import bot  

# Scale factor
SCALE = 2  # 2x upscale
# Document counter
doc_counter = 1

@bot.on_message(filters.command("up") & filters.reply & (filters.private | filters.group))
async def upscale_image(client, message: Message):
    global doc_counter

    replied = message.reply_to_message
    if not (replied.photo or replied.document):
        return await message.reply("❌ Please reply to a photo or image document to upscale it.")

    # Send temporary status message
    status_msg = await message.reply("🔄 Upscaling your image locally, please wait...")

    try:
        # Download the media
        file_path = await replied.download()
        img = Image.open(file_path)

        # Get new size
        new_size = (img.width * SCALE, img.height * SCALE)

        # Upscale using PIL (bicubic)
        upscaled = img.resize(new_size, Image.BICUBIC)

        # Save to buffer for sending as document
        buf_doc = BytesIO()
        upscaled.save(buf_doc, format="JPEG")
        buf_doc.seek(0)

        # Prepare document name
        doc_name = f"Alpha[{doc_counter}].jpg"
        doc_counter += 1

        # Delete temporary status message
        await status_msg.delete()

        # Send directly as document with caption
        await message.reply_document(buf_doc, file_name=doc_name, caption="✅ ɪᴍᴀɢᴇ ᴜᴘꜱᴄᴀʟᴇᴅ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ")

    except Exception as e:
        await status_msg.edit_text(f"❌ Upscale failed.\nError: `{e}`")