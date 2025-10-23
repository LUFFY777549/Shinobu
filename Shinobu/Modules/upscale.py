# Shinobu/Modules/upscale.py
import asyncio
from io import BytesIO
import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from Shinobu import bot  # Tumhara Shinobu Pyrogram bot object

PHOTOAI_UPLOAD = "https://photoai.imglarger.com/api/PhoAi/Upload"
PHOTOAI_STATUS = "https://photoai.imglarger.com/api/PhoAi/CheckStatus"

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "referer": "https://image-enhancer-snowy.vercel.app/",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site"
}

@bot.on_message(filters.command("up") & filters.reply & (filters.private | filters.group))
async def upscale_image(client, message: Message):
    if not message.reply_to_message.photo:
        return await message.reply("❌ Please reply to a photo to upscale it.")

    status_msg = await message.reply("🔄 Upscaling your image, please wait...")

    try:
        # Download the replied photo
        file_path = await message.reply_to_message.download()
        with open(file_path, "rb") as f:
            image_data = BytesIO(f.read())

        # Upload image to PhotoAI
        form = aiohttp.FormData()
        form.add_field("type", "1")
        form.add_field("scaleRadio", "1")
        form.add_field("file", image_data, filename="image.jpg", content_type="image/jpeg")

        async with aiohttp.ClientSession() as session:
            async with session.post(PHOTOAI_UPLOAD, data=form, headers=HEADERS) as upload_resp:
                upload_json = await upload_resp.json()
                code = upload_json["data"]["code"]

            # Poll for status until ready
            while True:
                payload = {"type": "2", "code": code}
                async with session.post(PHOTOAI_STATUS, json=payload, headers=HEADERS) as status_resp:
                    status_json = await status_resp.json()
                    if "data" in status_json and "downloadUrls" in status_json["data"]:
                        download_url = status_json["data"]["downloadUrls"][0]
                        if download_url.endswith(f"{code}.jpg"):
                            await status_msg.edit_text("✅ Image upscaled successfully!")
                            await message.reply_photo(download_url, caption="Here is your upscaled image!")
                            return
                await asyncio.sleep(3)

    except Exception as e:
        await status_msg.edit_text(f"❌ Upscale failed.\nError: `{e}`")