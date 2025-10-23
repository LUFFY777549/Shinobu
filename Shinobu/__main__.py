# Shinobu/__main__.py
from pyrogram import Client
import os
from pytgcalls import PyTgCalls
from pytgcalls.types import InputStream, InputAudioStream  # check your version
from config import API_ID, API_HASH, BOT_TOKEN
from pyrogram.session import StringSession
from pyrogram.raw.all import layer

# create bot client (bot account — for messages)
bot = Client("shinobu_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins={"root":"Shinobu.Modules"})

# create user client (userbot) from string session (for VC)
STRING_SESSION = os.environ.get("STRING_SESSION")
if not STRING_SESSION:
    raise RuntimeError("STRING_SESSION required for VC streaming")

user = Client(StringSession(STRING_SESSION), api_id=API_ID, api_hash=API_HASH, plugins={"root":"Shinobu.Modules"})

# pytgcalls instance bound to user client
call = PyTgCalls(user)

if __name__ == "__main__":
    user.start()   # start both clients
    bot.start()
    call.start()
    bot.idle()
    # on shutdown:
    call.stop()
    user.stop()
    bot.stop()