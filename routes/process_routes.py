# routes/process_routes.py
from flask import Blueprint, render_template, request
from config import Config
from sheets import update_google_sheet
from videos import get_video_id, get_playlist_id
from helpers import fetch_details
from validation import validate_youtube_url
import logging

process_bp = Blueprint('process', __name__)

logger = logging.getLogger(__name__)

config = Config()

@process_bp.route('/process', methods=['POST'])
def process():
    url = request.form['url']
    
    # Validate URL
    error_message = validate_youtube_url(url)
    if error_message:
        logger.error(f"Invalid URL submitted: {url}")
        return render_template('index.html', error_message=error_message)

    video_id = get_video_id(url)
    playlist_id = get_playlist_id(url)

    # Handle case where both video_id and playlist_id are present
    if video_id and playlist_id:
        return render_template('index.html', url_contains_both=True, url=url)
    
    # Fetch details
    error_message, success_message, details_list = fetch_details(video_id, playlist_id)
    if error_message:
        logger.error(f"Error processing URL: {url} - {error_message}")
        return render_template('index.html', error_message=error_message)
    
    update_google_sheet(details_list)
    return render_template('index.html', success_message=success_message)
