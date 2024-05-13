# YouTube to Google Sheets

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

## Required setup

1. **Create a `.env` file in the root directory with the following contents:**

   ```env
   YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
   GOOGLE_CREDENTIALS=path/to/your/service-account-credentials.json
   SPREADSHEET_NAME=Your Google Sheet Name
   SHEET_NAME=Sheet1
   ```

   - Replace `YOUR_YOUTUBE_API_KEY` with your actual YouTube Data API key.
   - Replace `path/to/your/service-account-credentials.json` with the path to your Google service account credentials JSON file.
   - Replace `Your Google Sheet Name` with the name of your Google Sheets document.
   - Replace `Sheet1` with the name of the sheet within the Google Sheets document.

2. **Keep your .env file and credentials JSON file secure and do not share them publicly. If you fork this project, ensure your `.gitignore` file includes the following to avoid committing sensitive information:**

   ```gitignore
   .env
   credentials.json
   ```

3. **Ensure that your Google service account has the necessary permissions to access and edit the specified Google Sheets document.**

   - Open your Google Sheets document.

   - Click the "Share" button in the top-right corner.

   - Enter the service account email (found in the client_email field of your service-account-credentials.json file) and share the document with it, giving it at least "Editor" access.

## Usage

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

2. **Open your web browser and go to `http://127.0.0.1:5000/`.**

3. **Enter a YouTube URL (video or playlist) and submit the form.**

   If the URL contains both a video ID and a playlist ID, you will be prompted to choose whether to add just the video or the entire playlist.

   The application will fetch the video details and update the specified Google Sheets document.

## Project Structure

- `app.py`: Main application file containing the Flask app and logic for fetching video details and updating Google Sheets.
- `templates/index.html`: HTML template for the web form and user interface.
- `.env`: Environment variables file (should be created manually as per instructions).
- `.gitignore`: Git ignore file to exclude sensitive files from being committed.
- `requirements.txt`: List of dependencies.

## License

This project is licensed under the MIT License.

## Conclusion

By following this README, you can set up and run your YouTube to Google Sheets application securely and efficiently. This documentation includes all necessary details to help you or any other user understand and use the application effectively.
