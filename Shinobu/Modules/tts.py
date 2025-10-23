# Shinobu/Modules/tts.py
from pyrogram import filters
from gtts import gTTS
from Shinobu import bot  # Tumhara Pyrogram bot object

@bot.on_message(filters.command("tts") & (filters.private | filters.group))
def tts_convert(client, message):
    if len(message.command) < 2:
        return message.reply_text("❌ Usage: /tts <text>")

    text = message.text.split(' ', 1)[1]

    # Generate TTS in Hindi
    tts = gTTS(text=text, lang='hi')
    tts.save('speech.mp3')

    # Agar reply hai to replied message ke liye reply kare
    if message.reply_to_message:
        client.send_audio(
            chat_id=message.chat.id,
            audio="speech.mp3",
            reply_to_message_id=message.reply_to_message.message_id,
            caption=f"TTS for: {text[:50]}..."
        )
    else:
        client.send_audio(
            chat_id=message.chat.id,
            audio="speech.mp3",
            caption=f"TTS for: {text[:50]}..."
        )