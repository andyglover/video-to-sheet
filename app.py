from flask import Flask, request, render_template
from config import Config
from sheets import update_google_sheet
from videos import is_valid_youtube_url, get_video_id, get_playlist_id, get_video_details, get_playlist_videos
import logging


# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Instantiate Config and validate environment variables
try:
    config = Config()
except EnvironmentError as e:
    logger.error(f"Configuration validation failed: {str(e)}")
    raise

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    url = request.form['url']
    video_id = get_video_id(url)
    playlist_id = get_playlist_id(url)

    if not is_valid_youtube_url(url):
        error_message = "Invalid YouTube URL. Please enter a valid URL."
        logger.error(f"Invalid URL submitted: {url}")
        return render_template('index.html', error_message=error_message)

    if video_id and playlist_id:
        return render_template('index.html', url_contains_both=True, url=url)
    elif playlist_id:
        video_details_list = get_playlist_videos(playlist_id)
        if not video_details_list:
            error_message = "Unable to fetch playlist details. Please check the playlist URL."
            logger.error(f"Failed to fetch details for playlist: {url}")
            return render_template('index.html', error_message=error_message)
        update_google_sheet(video_details_list)
        success_message = f"Details saved for {len(video_details_list)} videos."
        return render_template('index.html', success_message=success_message)
    elif video_id:
        video_details_list = get_video_details(video_id)
        if not video_details_list:
            error_message = "Unable to fetch video details. Please check the video URL."
            logger.error(f"Failed to fetch details for video: {url}")
            return render_template('index.html', error_message=error_message)
        update_google_sheet(video_details_list)
        success_message = "Details saved for 1 video."
        return render_template('index.html', success_message=success_message)
    else:
        error_message = "Unable to extract video or playlist ID from URL."
        logger.error(f"Invalid URL without identifiable video or playlist ID: {url}")
        return render_template('index.html', error_message=error_message)

@app.route('/confirm', methods=['POST'])
def confirm():
    url = request.form['url']
    option = request.form.get('option', 'single')

    if not is_valid_youtube_url(url):
        error_message = "Invalid YouTube URL. Please enter a valid URL."
        logger.error(f"Invalid URL submitted: {url}")
        return render_template('index.html', error_message=error_message)

    video_id = get_video_id(url)
    playlist_id = get_playlist_id(url)
    if option == 'single':
        video_details_list = get_video_details(video_id)
    else:
        video_details_list = get_playlist_videos(playlist_id)

    update_google_sheet(video_details_list)
    success_message = f"Details saved for {len(video_details_list)} videos."
    return render_template('index.html', success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)
