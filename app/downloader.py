import os
from yt_dlp import YoutubeDL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

def download_video(url: str) -> str:
    is_tiktok = "tiktok.com" in url.lower()

    ydl_opts = {
        "outtmpl": os.path.join(VIDEOS_DIR, "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "ffmpeg_location": "/usr/bin/ffmpeg",
        "format": "bv*[vcodec!=none]+ba[acodec!=none]/best",
    }

    if is_tiktok:
        ydl_opts["format"] = "bv*+ba/best"

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join(VIDEOS_DIR, f"{info['id']}.mp4")
