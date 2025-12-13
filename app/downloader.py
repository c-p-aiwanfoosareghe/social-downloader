import os
from yt_dlp import YoutubeDL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

FFMPEG_PATH = "/usr/bin/ffmpeg"  # explicit path

def download_video(url: str) -> str:
    url_l = url.lower()
    is_tiktok = "tiktok.com" in url_l

    ydl_opts = {
        "outtmpl": os.path.join(VIDEOS_DIR, "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": False,  # 🔴 enable logs
        "merge_output_format": "mp4",
        "ffmpeg_location": FFMPEG_PATH,
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
        ],
    }

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
        # 🔴 FORCE DASH MERGE
        ydl_opts.update({
            "format": "bv*[vcodec!=none]+ba[acodec!=none]/best",
        })

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"/videos/{info['id']}.mp4"
