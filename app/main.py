import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl

from app.downloader import download_video

app = FastAPI(title="Universal Video Downloader")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

os.makedirs(VIDEOS_DIR, exist_ok=True)

# ------------------ MODELS ------------------
class DownloadRequest(BaseModel):
    url: HttpUrl

# ------------------ API ------------------
@app.post("/api/download")
def download(req: DownloadRequest):
    try:
        video_path = download_video(str(req.url))
        filename = os.path.basename(video_path)

        return {
            "ok": True,
            "download_url": f"/download/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------ FILE DOWNLOAD (IOS SAFE) ------------------
@app.get("/download/{filename}")
def download_file(filename: str):
    path = os.path.join(VIDEOS_DIR, filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path,
        media_type="video/mp4",
        filename=filename,          # 🔴 forces Safari download
        headers={"Cache-Control": "no-store"}
    )

# ------------------ FRONTEND ------------------
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
