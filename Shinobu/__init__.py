# __init__.py
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import logging

bot = Client(
    "ShinoBuBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Shinobu/Modules")
)

logging.basicConfig(
  format="[Alpha-Bot] %(name)s - %(levelname)s - %(message)s",
  handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
  level=logging.INFO,
)