import os
from yt_dlp import YoutubeDL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

def download_video(url: str) -> str:
    url_l = url.lower()
    is_tiktok = "tiktok.com" in url_l

    ydl_opts = {
        "outtmpl": os.path.join(VIDEOS_DIR, "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
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
        ydl_opts.update({
            "format": "(bv*+ba/best)/best",
        })

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = f"{info['id']}.mp4"
        return f"/videos/{filename}"
