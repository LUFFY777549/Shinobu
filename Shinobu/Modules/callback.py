# Shinobu/Modules/callbacks.py
from pyrogram import filters
from pyrogram.types import CallbackQuery
from Shinobu import bot, call

@bot.on_callback_query(filters.regex(r"^(pause|skip|stop|close)\|(.+)$"))
async def controls(_, query: CallbackQuery):
    action, chat = query.data.split("|")
    chat_id = int(chat)
    if action == "pause":
        await call.pause_stream(chat_id)
        await query.answer("Paused")
    elif action == "skip":
        # implement queue skip logic
        await query.answer("Skipped")
    elif action == "stop":
        await call.leave_group_call(chat_id)
        await query.answer("Stopped")
    elif action == "close":
        await query.message.delete()
        await query.answer("Closed")