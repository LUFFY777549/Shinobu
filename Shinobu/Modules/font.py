from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Shinobu import bot  # Your Pyrogram client
from Shinobu.fonts import fonts  # import fonts.py

# Command /font or /fonts
@bot.on_message(filters.command(["font", "fonts"]))
async def font_buttons(client, message, cb=False):
    buttons = [
        [
            InlineKeyboardButton("Typewriter", callback_data="style+typewriter"),
            InlineKeyboardButton("Outline", callback_data="style+outline"),
            InlineKeyboardButton("Serif", callback_data="style+serif"),
        ],
        [
            InlineKeyboardButton("Bold", callback_data="style+bold_cool"),
            InlineKeyboardButton("SmallCaps", callback_data="style+small_cap"),
        ],
        [InlineKeyboardButton("Next ➻", callback_data="nxt")],
    ]
    if not cb:
        await message.reply_text(
            message.text or "Select a font style:",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.edit_reply_markup(InlineKeyboardMarkup(buttons))

# Callback for next page or style selection
@bot.on_callback_query(filters.regex("^style|^nxt"))
async def style_callback(client, callback_query):
    data = callback_query.data
    await callback_query.answer()
    
    if data.startswith("style+"):
        _, style = data.split("+")
        text = callback_query.message.reply_to_message.text
        func = getattr(fonts, style, None)
        if func:
            new_text = func(text)
            await callback_query.message.edit_text(new_text, reply_markup=callback_query.message.reply_markup)
    elif data == "nxt":
        # example next page buttons
        buttons = [
            [InlineKeyboardButton("Comic", callback_data="style+comic"),
             InlineKeyboardButton("Script", callback_data="style+script")],
            [InlineKeyboardButton("Back ◀", callback_data="back")]
        ]
        await callback_query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
    elif data == "back":
        await font_buttons(client, callback_query, cb=True)