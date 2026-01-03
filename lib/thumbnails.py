# lib/thumbnail.py
import os
from moviepy import VideoFileClip
from PIL import Image
from lib.constants import CACHE_DIR, WALLPAPER_DIR

def get_thumbnail(video_name: str) -> str:
    """
    Returns the path to a thumbnail for the given video.
    Generates it if missing.
    """
    # remove extension for thumbnail file name
    file_name = os.path.splitext(video_name)[0] + ".png"
    thumb_path = os.path.join(CACHE_DIR, file_name)
    video_path = os.path.join(WALLPAPER_DIR, video_name)


    if not os.path.exists(thumb_path):
        try:
            with VideoFileClip(video_path) as clip:
                frame = clip.get_frame(0.0)
                img = Image.fromarray(frame)
                img.save(thumb_path, "PNG")
        except Exception as e:
            print(f"Failed to make thumbnail for {video_name}: {e}")
            return None
    return thumb_path
