# routes/main_routes.py
from flask import Blueprint, render_template, request
from config import Config
from sheets import update_google_sheet
from videos import get_video_id, get_playlist_id, get_video_details, get_playlist_videos
from helpers import fetch_details
from validation import validate_youtube_url  # Import validation functions
import logging

main_bp = Blueprint('main', __name__)

logger = logging.getLogger(__name__)

config = Config()

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main_bp.route('/process', methods=['POST'])
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

@main_bp.route('/confirm', methods=['POST'])
def confirm():
    url = request.form['url']
    option = request.form.get('option', 'single')

    # Validate URL
    error_message = validate_youtube_url(url)
    if error_message:
        logger.error(f"Invalid URL submitted: {url}")
        return render_template('index.html', error_message=error_message)

    video_id = get_video_id(url)
    playlist_id = get_playlist_id(url)
    if option == 'single':
        video_details_list = get_video_details(video_id)
    else:
        video_details_list = get_playlist_videos(playlist_id)

    if not video_details_list:
        error_message = "Failed to fetch video/playlist details. Please check the URL and try again."
        logger.error(f"Error fetching details for URL: {url}")
        return render_template('index.html', error_message=error_message)

    update_google_sheet(video_details_list)
    success_message = f"Details saved for {len(video_details_list)} videos."
    return render_template('index.html', success_message=success_message)
