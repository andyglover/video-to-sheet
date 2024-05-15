# validation.py
import re

def is_valid_youtube_url(url):
    youtube_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    )
    return re.match(youtube_regex, url) is not None

def validate_youtube_url(url):
    if not url or len(url) > 2048 or not is_valid_youtube_url(url):
        return "Invalid YouTube URL. Please enter a valid URL in the correct format."
    return None
