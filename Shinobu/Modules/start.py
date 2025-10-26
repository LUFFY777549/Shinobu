from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Shinobu import bot
from Shinobu.db import Users, Groups

START_IMAGE = "https://files.catbox.moe/xa33dy.jpg"
START_TIME = datetime.utcnow()

def get_uptime():
    delta = datetime.utcnow() - START_TIME
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h:{minutes}m:{seconds}s"

@bot.on_message(filters.command("start") & filters.private)
async def start_private(client, message):
    user = message.from_user
    await Users.update_one(
        {"user_id": user.id},
        {"$set": {"username": user.username, "joined_at": datetime.utcnow()}},
        upsert=True
    )

    uptime = get_uptime()
    caption = (
    f"Hey {user.mention}!\n"
    "๏ ᴛʜɪs ɪs 「sʜɪɴᴏʙᴜ X ᴄʜᴀᴛʙᴏᴛ🦋」!\n"
    "➻ ᴀ sᴍᴀʀᴛ & ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀᴛʙᴏᴛ ᴡɪᴛʜ ʟᴏᴛs ᴏꜰ ᴜsᴇꜰᴜʟ ꜰᴇᴀᴛᴜʀᴇs.\n\n"
    "Sᴜᴘᴘᴏʀᴛᴇᴅ Fᴇᴀᴛᴜʀᴇs : ʀᴇᴍɪɴᴅᴇʀs, ɴᴏᴛᴇs, ᴄʜᴀᴛ ᴍᴏᴅᴜʟᴇs, ᴀɴᴅ ᴍᴜᴄʜ ᴍᴏʀᴇ.\n"
    "──────────────────\n"
    "๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ᴍᴏᴅᴜʟᴇs."
)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("ADD ME TO YOUR GROUP", url="https://t.me/YourBot?startgroup=true")],
        [
            InlineKeyboardButton("OWNER", url="https://t.me/YourUsername"),
            InlineKeyboardButton("UPDATES", url="https://t.me/YourUpdatesChannel")
        ],
        [InlineKeyboardButton("HELP AND COMMANDS", callback_data="help_cmds")]
    ])

    await client.send_photo(message.chat.id, START_IMAGE, caption=caption, reply_markup=buttons)

@bot.on_message(filters.command("start") & filters.group)
async def start_group(client, message):
    await Groups.update_one(
        {"group_id": message.chat.id},
        {"$set": {"group_name": message.chat.title, "joined_at": datetime.utcnow()}},
        upsert=True
    )
    await message.reply_text("「sʜɪɴᴏʙᴜ X ᴄʜᴀᴛʙᴏᴛ🦋」 is now active in this group!")