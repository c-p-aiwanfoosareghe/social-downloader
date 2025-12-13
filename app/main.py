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
    ydl_opts = {
        "format": "mp4/best",
        "outtmpl": os.path.join(VIDEOS_DIR, "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = f"{info['id']}.mp4"
        platform = info.get("extractor", "unknown")
        return f"/videos/{filename}", platform

# ---------------- API ----------------
@app.post("/scrape")
def scrape(req: DownloadRequest):
    try:
        video_url, platform = download_video(str(req.url))
        return {
            "ok": True,
            "data": {
                "platform": platform,
                "video_url": video_url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- STATIC ----------------
app.mount("/videos", StaticFiles(directory=VIDEOS_DIR), name="videos")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
