import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from yt_dlp import YoutubeDL
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Universal Reel Downloader")

# -------------------------
# Config
# -------------------------
VIDEOS_DIR = "videos"
os.makedirs(VIDEOS_DIR, exist_ok=True)

# -------------------------
# Models
# -------------------------
class ReelsRequest(BaseModel):
    url: HttpUrl

# -------------------------
# Downloader (Watermark-aware)
# -------------------------
def download_video(url: str):
    is_tiktok = "tiktok.com" in url.lower()

    ydl_opts = {
        "outtmpl": os.path.join(VIDEOS_DIR, "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
    }

    if is_tiktok:
        # ✅ TikTok NO watermark
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
        return f"/videos/{filename}"

# -------------------------
# API ROUTES (FIRST)
# -------------------------
@app.post("/scrape")
def scrape(req: ReelsRequest):
    try:
        video_url = download_video(str(req.url))
        return {
            "ok": True,
            "data": {
                "url": str(req.url),
                "status": "Downloaded successfully",
                "video_url": video_url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"ok": True}

# -------------------------
# Static Files (LAST)
# -------------------------
app.mount("/videos", StaticFiles(directory=VIDEOS_DIR), name="videos")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
