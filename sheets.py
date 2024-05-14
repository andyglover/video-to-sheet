import gspread
from config import Config
import logging

logger = logging.getLogger(__name__)
config = Config()

def update_google_sheet(data):
    gc = gspread.service_account(filename=config.CREDENTIALS_FILE)
    
    sheet_list = gc.openall()
    logger.info("Available Spreadsheets:")
    for sheet in sheet_list:
        logger.info(sheet.title)
    
    try:
        sheet = gc.open(config.SPREADSHEET_NAME).worksheet(config.SHEET_NAME)
    except gspread.SpreadsheetNotFound:
        logger.error(f"Spreadsheet '{config.SPREADSHEET_NAME}' not found.")
        raise
    except gspread.WorksheetNotFound:
        logger.error(f"Worksheet '{config.SHEET_NAME}' not found in spreadsheet '{config.SPREADSHEET_NAME}'.")
        raise

    for row in data:
        sheet.append_row([row["title"], row["channel"], row["duration"], row["url"]])
