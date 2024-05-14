import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class Config:
    def __init__(self):
        # Load API key and credentials path from environment variables
        self.API_KEY = os.getenv('YOUTUBE_API_KEY')
        self.CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS')
        self.SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME')
        self.SHEET_NAME = os.getenv('SHEET_NAME')
        self.validate()

    def validate(self):
        missing_vars = [var for var in ['YOUTUBE_API_KEY', 'GOOGLE_CREDENTIALS', 'SPREADSHEET_NAME', 'SHEET_NAME'] if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

