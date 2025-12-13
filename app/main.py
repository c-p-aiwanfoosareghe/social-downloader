import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from yt_dlp import YoutubeDL
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Social Media Downloader")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

os.makedirs(VIDEOS_DIR, exist_ok=True)

# ---------------- MODELS ----------------
class DownloadRequest(BaseModel):
    url: HttpUrl

# ---------------- DOWNLOAD LOGIC ----------------
def download_video(url: str):
    is_tiktok = "tiktok.com" in url.lower()

    ydl_opts = {
        "outtmpl": os.path.join(VIDEOS_DIR, "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "nocheckcertificate": True,
    }

    # 🔥 TikTok: force no-watermark formats
    if is_tiktok:
        ydl_opts.update({
            "format": "bv*+ba/best",
            "extractor_args": {
                "tiktok": {
                    "api_hostname": "api16-normal-c-useast1a.tiktokv.com",
                    "app_version": "26.1.3",
                }
            }
        })
    else:
        # Instagram / Facebook / Threads
        ydl_opts.update({
            "format": "bestvideo+bestaudio/best"
        })

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = f"{info['id']}.mp4"
        platform = info.get("extractor", "unknown")

        return f"/videos/{filename}", platform
