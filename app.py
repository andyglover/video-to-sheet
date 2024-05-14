from flask import Flask, request, render_template
from googleapiclient.discovery import build
from dotenv import load_dotenv
from config import Config
import gspread
import isodate

# Load environment variables from .env file
load_dotenv()

# Instantiate Config and validate environment variables
config = Config()

app = Flask(__name__)

# Function to get video details from YouTube
def get_video_details(video_ids):
    youtube = build('youtube', 'v3', developerKey=config.API_KEY)
    
    if isinstance(video_ids, str):
        video_ids = [video_ids]
    
    request = youtube.videos().list(
        part="snippet,contentDetails",
        id=','.join(video_ids)
    )
    response = request.execute()
    
    video_details_list = []
    for video in response['items']:
        title = video['snippet']['title']
        channel = video['snippet']['channelTitle']
        duration_iso = video['contentDetails']['duration']
        duration = isodate.parse_duration(duration_iso)
        
        # Convert duration to a human-readable format
        minutes, seconds = divmod(duration.total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            duration_str = f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"
        else:
            duration_str = f"{int(minutes)}:{int(seconds):02}"
        
        video_details_list.append({
            "title": title,
            "channel": channel,
            "duration": duration_str,
            "url": f"https://www.youtube.com/watch?v={video['id']}"
        })
    
    return video_details_list

# Function to get all video IDs from a playlist
def get_playlist_videos(playlist_id):
    youtube = build('youtube', 'v3', developerKey=config.API_KEY)
    
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response['items']:
            video_id = item['contentDetails']['videoId']
            video_ids.append(video_id)
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    # Fetch video details in bulk using the unified function
    video_details_list = get_video_details(video_ids)
    
    return video_details_list

# Function to update Google Sheets
def update_google_sheet(data):
    gc = gspread.service_account(filename=config.CREDENTIALS_FILE)
    
    # Print available spreadsheets for debugging
    sheet_list = gc.openall()
    print("Available Spreadsheets:")
    for sheet in sheet_list:
        print(sheet.title)
    
    # Open the specified spreadsheet and sheet
    try:
        sheet = gc.open(config.SPREADSHEET_NAME).worksheet(config.SHEET_NAME)
    except gspread.SpreadsheetNotFound:
        print(f"Spreadsheet '{config.SPREADSHEET_NAME}' not found.")
        raise
    except gspread.WorksheetNotFound:
        print(f"Worksheet '{config.SHEET_NAME}' not found in spreadsheet '{config.SPREADSHEET_NAME}'.")
        raise

    for row in data:
        sheet.append_row([row["title"], row["channel"], row["duration"], row["url"]])

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    url = request.form['url']
    if "watch" in url and "list=" in url:
        return render_template('index.html', url_contains_both=True, url=url)
    elif "playlist" in url:
        playlist_id = url.split("list=")[-1].split('&')[0]
        video_details_list = get_playlist_videos(playlist_id)
        update_google_sheet(video_details_list)
        success_message = f"Details saved for {len(video_details_list)} videos."
        return render_template('index.html', success_message=success_message)
    else:
        video_id = url.split("v=")[-1].split('&')[0]
        video_details_list = get_video_details(video_id)
        update_google_sheet(video_details_list)
        success_message = "Details saved for 1 video."
        return render_template('index.html', success_message=success_message)

@app.route('/confirm', methods=['POST'])
def confirm():
    url = request.form['url']
    option = request.form.get('option', 'single')
    video_id = url.split("v=")[-1].split('&')[0]
    playlist_id = url.split("list=")[-1].split('&')[0]
    if option == 'single':
        video_details_list = get_video_details(video_id)
    else:
        video_details_list = get_playlist_videos(playlist_id)
    
    update_google_sheet(video_details_list)
    success_message = f"Details saved for {len(video_details_list)} videos."
    return render_template('index.html', success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)
