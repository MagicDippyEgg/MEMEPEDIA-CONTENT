import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Authenticate using Google Drive API credentials
creds = Credentials.from_authorized_user_info(
    client_id=os.getenv('GOOGLE_DRIVE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_DRIVE_CLIENT_SECRET'),
    refresh_token=os.getenv('GOOGLE_DRIVE_REFRESH_TOKEN')
)

# Set up Google Drive service
drive_service = build('drive', 'v3', credentials=creds)

# List files in Google Drive to verify connection
results = drive_service.files().list(pageSize=5).execute()
files = results.get('files', [])

if not files:
    print('No files found.')
else:
    for file in files:
        print(f"File ID: {file['id']}, Name: {file['name']}")
