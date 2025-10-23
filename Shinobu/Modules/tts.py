# tts.py
from pyrogram import filters
from Shinobu import bot
from gtts import gTTS
from io import BytesIO

@bot.on_message(filters.command("tts") & (filters.private | filters.group))
async def tts_convert(client, message):
    # User ka text
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: /tts <text>")
    
    text = message.text.split(None, 1)[1]

    # TTS generate
    tts = gTTS(text=text, lang='en')
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)

    # Send audio file
    await message.reply_audio(audio_file, file_name="tts.mp3", caption=f"TTS for: {text[:50]}...")