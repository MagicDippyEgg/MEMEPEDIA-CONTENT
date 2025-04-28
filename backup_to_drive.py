import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Get environment variables
client_id = os.getenv('GOOGLE_DRIVE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_DRIVE_CLIENT_SECRET')
refresh_token = os.getenv('GOOGLE_DRIVE_REFRESH_TOKEN')

# Make sure credentials are set correctly
if not all([client_id, client_secret, refresh_token]):
    raise ValueError("Missing one or more required environment variables")

# Using the Credentials object with correct parameters
creds = Credentials.from_authorized_user_info(
    client_id=client_id,
    client_secret=client_secret,
    refresh_token=refresh_token
)

# Create the Google Drive service object
drive_service = build('drive', 'v3', credentials=creds)

# Example: List the files in the drive
results = drive_service.files().list(pageSize=5).execute()
items = results.get('files', [])

if not items:
    print("No files found.")
else:
    print('Files:')
    for item in items:
        print(f"{item['name']} ({item['id']})")
