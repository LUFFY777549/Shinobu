# ping.py
from datetime import datetime
import psutil
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Shinobu import bot

START_TIME = datetime.utcnow()
PING_IMAGE = "https://files.catbox.moe/xa33dy.jpg"  # Replace with your desired image URL

def get_uptime():
    delta = datetime.utcnow() - START_TIME
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h:{minutes}m:{seconds}s"

async def send_ping(client, message):
    user_mention = message.from_user.mention if message.from_user else "User"

    # System stats
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=0.5)
    disk = psutil.disk_usage('/').percent
    uptime = get_uptime()

    # Ping calculation
    start = datetime.utcnow()
    msg = await message.reply_text("🏓 Pinging...")
    end = datetime.utcnow()
    ping = (end - start).total_seconds() * 1000  # in ms

    caption = (
        f"➻ ᴩᴏɴɢ : {ping:.3f}ᴍs\n\n"
        f"「sʜɪɴᴏʙᴜ X ᴄʜᴀᴛʙᴏᴛ 🦋」 sʏsᴛᴇᴍ sᴛᴀᴛs :\n\n"
        f"๏ ᴜᴩᴛɪᴍᴇ : {uptime}\n"
        f"๏ ʀᴀᴍ : {ram}\n"
        f"๏ ᴄᴩᴜ : {cpu}\n"
        f"๏ ᴅɪsᴋ : {disk}\n"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("SUPPORT", url="https://t.me/YourSupportChannel")]
    ])

    await msg.delete()
    await client.send_photo(chat_id=message.chat.id, photo=PING_IMAGE, caption=caption, reply_markup=buttons)


# Private chat
@bot.on_message(filters.command("ping") & filters.private)
async def ping_private(client, message):
    await send_ping(client, message)

# Group chat
@bot.on_message(filters.command("ping") & filters.group)
async def ping_group(client, message):
    await send_ping(client, message)