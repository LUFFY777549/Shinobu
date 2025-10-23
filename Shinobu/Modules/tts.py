# tts.py
from pyrogram import filters
from pyrogram.types import InputFile
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

    # Wrap BytesIO in InputFile with filename
    input_audio = InputFile(audio_file, filename="tts.mp3")

    # Send audio
    await message.reply_audio(
        input_audio,
        caption=f"TTS for: {text[:50]}..."
    )