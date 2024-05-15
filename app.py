# app.py
from flask import Flask
from config import Config
import logging
from routes.main_routes import main_bp
from routes.process_routes import process_bp  # Import process blueprint
from routes.confirm_routes import confirm_bp  # Import confirm blueprint

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
app.register_blueprint(process_bp)  # Register process blueprint
app.register_blueprint(confirm_bp)  # Register confirm blueprint

if __name__ == '__main__':
    app.run(debug=True)
