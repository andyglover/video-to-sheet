from flask import Flask, request, render_template
from config import Config
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
