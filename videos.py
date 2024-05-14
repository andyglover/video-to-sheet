import re
from googleapiclient.discovery import build
import isodate
from config import Config
import logging

logger = logging.getLogger(__name__)
config = Config()

def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    )
    return re.match(youtube_regex, url) is not None

def get_video_id(url):
    video_id = re.search(r'(?<=v=)[^&#]+', url)
    return video_id.group(0) if video_id else None

def get_playlist_id(url):
    playlist_id = re.search(r'(?<=list=)[^&#]+', url)
    return playlist_id.group(0) if playlist_id else None

def get_video_details(video_ids):
    youtube = build('youtube', 'v3', developerKey=config.API_KEY)
    
    if isinstance(video_ids, str):
        video_ids = [video_ids]
    
    request = youtube.videos().list(
        part="snippet,contentDetails",
        id=','.join(video_ids)
    )
    response = request.execute()
    
    video_details_list = []
    for video in response['items']:
        title = video['snippet']['title']
        channel = video['snippet']['channelTitle']
        duration_iso = video['contentDetails']['duration']
        duration = isodate.parse_duration(duration_iso)
        
        minutes, seconds = divmod(duration.total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            duration_str = f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"
        else:
            duration_str = f"{int(minutes)}:{int(seconds):02}"
        
        video_details_list.append({
            "title": title,
            "channel": channel,
            "duration": duration_str,
            "url": f"https://www.youtube.com/watch?v={video['id']}"
        })
    
    return video_details_list

def get_playlist_videos(playlist_id):
    youtube = build('youtube', 'v3', developerKey=config.API_KEY)
    
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response['items']:
            video_id = item['contentDetails']['videoId']
            video_ids.append(video_id)
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    video_details_list = get_video_details(video_ids)
    
    return video_details_list
