# tts.py (Pyrogram 2.x compatible)
from pyrogram import filters
from Shinobu import bot
from gtts import gTTS
from io import BytesIO

@bot.on_message(filters.command("tts") & (filters.private | filters.group))
async def tts_convert(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: /tts <text>")
    
    text = message.text.split(None, 1)[1]

    # Generate TTS
    tts = gTTS(text=text, lang='en')
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)

    # Pyrogram 2.x compatible: file_name argument
    await message.reply_audio(
        audio_file,
        file_name="tts.mp3",
        caption=f"TTS for: {text[:50]}..."
    )