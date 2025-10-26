# Shinobu/Modules/upscale.py
import aiohttp
from io import BytesIO
from pyrogram import filters
from pyrogram.types import Message
from Shinobu import bot  # Your Pyrogram client

DEEPAI_API_URL = "https://api.deepai.org/api/torch-srgan"
DEEPAI_API_KEY = "485e1e55-860c-4f13-9a31-7fc0f85b3b4c"  # Get from https://deepai.org/

@bot.on_message(filters.command("up") & filters.reply & (filters.private | filters.group))
async def upscale_image(client, message: Message):
    if not message.reply_to_message.photo:
        return await message.reply("❌ Please reply to a photo to upscale it.")

    status_msg = await message.reply("🔄 Upscaling your image, please wait...")

    try:
        # Download photo
        file_path = await message.reply_to_message.download()
        with open(file_path, "rb") as f:
            image_data = BytesIO(f.read())

        headers = {"api-key": DEEPAI_API_KEY}

        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field("image", image_data, filename="image.jpg", content_type="image/jpeg")

            async with session.post(DEEPAI_API_URL, data=data, headers=headers) as resp:
                resp_json = await resp.json()

                if "output_url" in resp_json:
                    output_url = resp_json["output_url"]
                    await status_msg.edit_text("✅ Image upscaled successfully!")
                    await message.reply_photo(output_url, caption="Here is your upscaled image!")
                else:
                    await status_msg.edit_text(f"❌ Upscale failed. Response: {resp_json}")

    except Exception as e:
        await status_msg.edit_text(f"❌ Upscale failed.\nError: `{e}`")