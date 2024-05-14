from flask import Flask, request, render_template
from googleapiclient.discovery import build
import gspread
import isodate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load API key and credentials path from environment variables
API_KEY = os.getenv('YOUTUBE_API_KEY')
CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS')
SPREADSHEET_NAME = os.getenv('SPREADSHEET_NAME')
SHEET_NAME = os.getenv('SHEET_NAME')

# Function to get video details from YouTube
def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    request = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    )
    response = request.execute()
    
    video = response['items'][0]
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
    
    return {"title": title, "channel": channel, "duration": duration_str, "url": f"https://www.youtube.com/watch?v={video_id}"}

# Function to get all video IDs from a playlist
def get_playlist_videos(playlist_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    videos = []
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
            videos.append(get_video_details(video_id))
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return videos

# Function to update Google Sheets
def update_google_sheet(data):
    gc = gspread.service_account(filename=CREDENTIALS_FILE)
    
    # Print available spreadsheets for debugging
    sheet_list = gc.openall()
    print("Available Spreadsheets:")
    for sheet in sheet_list:
        print(sheet.title)
    
    # Open the specified spreadsheet and sheet
    try:
        sheet = gc.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)
    except gspread.SpreadsheetNotFound:
        print(f"Spreadsheet '{SPREADSHEET_NAME}' not found.")
        raise
    except gspread.WorksheetNotFound:
        print(f"Worksheet '{SHEET_NAME}' not found in spreadsheet '{SPREADSHEET_NAME}'.")
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
        video_details_list = [get_video_details(video_id)]
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
        video_details_list = [get_video_details(video_id)]
    else:
        video_details_list = get_playlist_videos(playlist_id)
    
    update_google_sheet(video_details_list)
    success_message = f"Details saved for {len(video_details_list)} videos."
    return render_template('index.html', success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)
