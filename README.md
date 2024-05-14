# video-to-sheet

This Flask application allows you to input YouTube video or playlist URLs and automatically fetches details such as title, channel name, duration, and URL. The fetched details are then added to a specified Google Sheets document.

## Features

- Fetches details for individual YouTube videos.
- Fetches details for all videos in a YouTube playlist.
- Option to choose between adding just a single video or an entire playlist if both are provided in the URL.
- Stores YouTube video details (title, channel name, duration, URL) in a specified Google Sheets document.
- Securely handles sensitive information using environment variables.

## Dependencies

The project requires the following Python libraries:

- Flask
- google-api-python-client
- gspread
- oauth2client
- isodate
- python-dotenv

  ```bash
  pip install Flask google-api-python-client gspread oauth2client isodate python-dotenv
  ```

  (Other sub-dependencies listed in the requirements.txt should be installed automatically when using pip.)

## Required setup

1. **Set up your own Google service account and YouTube Data API keys, and manage them securely and responsibly.**

### Google Sheets and Google Drive API

To enable the gspread library to modify a Google Sheet, enable Google Sheets and Google Drive API access using a Service Account as shown in the gspread docs: https://docs.gspread.org/en/latest/oauth2.html

Remember to share only the spreadsheet you want to modify with your service account:

- Open your Google Sheets document.

- Click the "Share" button in the top-right corner.

- Enter the service account email (found in the client_email field of your service-account-credentials.json file) and share the document with it, giving it at least "Editor" access.

### Youtube API

To enable retrieval of video and playlist information, enable Youtube Data API access via an API key, as shown in the Google Developer docs: https://developers.google.com/youtube/v3/getting-started

Remember to add restrictions to your API key to further secure it:

- From the API Dashboard "Credentials" page, choose the API key from the list.

- Under API restrictions, select YouTube Data API v3

More info: https://cloud.google.com/docs/authentication/api-keys#api_key_restrictions

### Environment Variables

This project uses environment variables for configuration. If any environment variables are missing, the application will print an error message and exit.

1. Create a `.env` file in the root directory with the following variables:

   ```env
   YOUTUBE_API_KEY=your_youtube_data_api_key
   GOOGLE_CREDENTIALS=your_google_service_account_credentials.json
   SPREADSHEET_NAME=your_google_sheets_document
   SHEET_NAME=Sheet1
   ```

   - Replace `Sheet1` with the name of the sheet within the Google Sheets document. (Sheet1 is usually the default for new Google Sheets)

2. Keep your .env file and credentials JSON file secure and do not share them publicly. If you track this code with git, ensure your `.gitignore` file includes the following to avoid committing sensitive information:

   ```gitignore
   .env
   credentials.json
   ```

## Usage

1. **Run the Flask application:**

   After setting up the environment variables and your API access, you can run the Flask application:

   ```bash
   python app.py
   ```

2. **Open your web browser and go to `http://127.0.0.1:5000/`.**

3. **Enter a YouTube URL (video or playlist) and submit the form.**

   If the URL contains both a video ID and a playlist ID, you will be prompted to choose whether to add just the video or the entire playlist.

   The application will fetch the video details and update the specified Google Sheets document.

## Project Structure

- `app.py`: Main application file containing the Flask app and logic for fetching video details and updating Google Sheets.
- `config.py`: Handles the loading and validation of environment variables. It ensures all necessary variables are set before the application runs.
- `templates/index.html`: HTML template for the web form and user interface.
- `.env`: Environment variables file (should be created manually as per instructions).
- `.gitignore`: Git ignore file to exclude sensitive files from being committed.
- `requirements.txt`: List of dependencies. (generated with "pip freeze > requirements.txt")

## License

This project is licensed under the MIT License.

## Disclaimer

This project is provided "as is" without warranty of any kind, express or implied. The user assumes all responsibility for using this project. It is the user's responsibility to ensure that their API keys and credentials are used responsibly, kept secure and not exposed publicly. The authors and maintainers of this project are not responsible for any misuse or damage that may occur from using this project.
