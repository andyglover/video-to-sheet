from videos import get_video_details, get_playlist_videos
import logging

logger = logging.getLogger(__name__)

def fetch_details(video_id, playlist_id):
    if playlist_id:
        details_list = get_playlist_videos(playlist_id)
        if not details_list:
            return "Unable to fetch playlist details. Please check the playlist URL.", None, None
        return None, f"Details saved for {len(details_list)} videos.", details_list
    elif video_id:
        details_list = get_video_details(video_id)
        if not details_list:
            return "Unable to fetch video details. Please check the video URL.", None, None
        return None, "Details saved for 1 video.", details_list
    else:
        return "Unable to extract video or playlist ID from URL.", None, None