from flask import Flask, request, render_template
from config import Config
from sheets import update_google_sheet
from videos import is_valid_youtube_url, get_video_id, get_playlist_id, get_video_details, get_playlist_videos
import logging
from routes.main_routes import main_bp

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

# Register Blueprints
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
