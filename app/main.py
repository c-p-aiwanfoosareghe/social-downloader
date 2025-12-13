import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl

from app.downloader import download_video

app = FastAPI(title="Universal Video Downloader")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

os.makedirs(VIDEOS_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: HttpUrl

# 🔹 API ROUTE (MUST BE FIRST)
@app.post("/api/download")
def download(req: DownloadRequest):
    try:
        video_url = download_video(str(req.url))
        return {"ok": True, "video_url": video_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 SERVE VIDEOS
app.mount("/videos", StaticFiles(directory=VIDEOS_DIR), name="videos")

# 🔹 SERVE FRONTEND (LAST!)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
