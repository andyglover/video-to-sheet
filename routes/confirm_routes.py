# routes/confirm_routes.py
from flask import Blueprint, render_template, request
from config import Config
from sheets import update_google_sheet
from videos import get_video_id, get_playlist_id, get_video_details, get_playlist_videos
from validation import validate_youtube_url
import logging

confirm_bp = Blueprint('confirm', __name__)

logger = logging.getLogger(__name__)

config = Config()

@confirm_bp.route('/confirm', methods=['POST'])
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
