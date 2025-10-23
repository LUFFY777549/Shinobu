#__main__.py
from pyrogram import Client, filters
from Shinobu import bot
from Shinobu.Modules import *

if __name__=="__main__":
    bot.run()
    with bot:
        bot.send_message(chat_id=7576729648,
                               text="BOT IS STARTED")