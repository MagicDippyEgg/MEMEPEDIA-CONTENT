import os
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Get environment variables
GOOGLE_DRIVE_CLIENT_ID = os.getenv("GOOGLE_DRIVE_CLIENT_ID")
GOOGLE_DRIVE_CLIENT_SECRET = os.getenv("GOOGLE_DRIVE_CLIENT_SECRET")
GOOGLE_DRIVE_REFRESH_TOKEN = os.getenv("GOOGLE_DRIVE_REFRESH_TOKEN")

# Check if any of the required environment variables are missing
if not GOOGLE_DRIVE_CLIENT_ID or not GOOGLE_DRIVE_CLIENT_SECRET or not GOOGLE_DRIVE_REFRESH_TOKEN:
    raise ValueError("Missing one or more required environment variables")

# Setup Google credentials
creds = Credentials(
    None,
    client_id=GOOGLE_DRIVE_CLIENT_ID,
    client_secret=GOOGLE_DRIVE_CLIENT_SECRET,
    refresh_token=GOOGLE_DRIVE_REFRESH_TOKEN
)

# Ensure the credentials are valid, refreshing if needed
if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())

# Build the Google Drive service
drive_service = build('drive', 'v3', credentials=creds)

# Example: List files in the Google Drive
try:
    results = drive_service.files().list(pageSize=5).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")
except Exception as e:
    print(f"An error occurred: {e}")
