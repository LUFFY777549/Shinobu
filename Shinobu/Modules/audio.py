# Shinobu/Modules/audio.py
import os
import asyncio
from yt_dlp import YoutubeDL
from datetime import timedelta
from pathlib import Path

YTDL_OPTS = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(id)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
    "restrictfilenames": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "geo_bypass": True
}

def ensure_dirs():
    Path("downloads").mkdir(parents=True, exist_ok=True)

def seconds_to_time(sec: int):
    td = timedelta(seconds=int(sec))
    h, m, s = td.seconds//3600, (td.seconds%3600)//60, td.seconds%60
    if td.days:
        h += td.days*24
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"

async def ytdl_download(query: str, cookies: str = None):
    ensure_dirs()
    loop = asyncio.get_event_loop()
    opts = YTDL_OPTS.copy()
    if cookies and os.path.exists(cookies):
        opts["cookiefile"] = cookies
    def run():
        with YoutubeDL(opts) as ydl:
            # ydl.extract_info can accept URLs or search:ytsearch1:query
            if query.startswith("http"):
                info = ydl.extract_info(query, download=True)
            else:
                info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            # if search, yt-dlp returns "entries"
            if "entries" in info:
                info = info["entries"][0]
            filename = ydl.prepare_filename(info)
            # convert to .mp3 / keep ext as is (we stream file with ffmpeg)
            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "duration": info.get("duration"),
                "filepath": filename,
                "thumbnail": info.get("thumbnail"),
                "webpage_url": info.get("webpage_url")
            }
    result = await loop.run_in_executor(None, run)
    return result