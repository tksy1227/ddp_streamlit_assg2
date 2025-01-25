import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = Credentials.from_authorized_user_file(token, SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        token.write(creds.to_json())

service = build('drive', 'v3', credentials=creds)

# Function to download all files in a folder
def download_folder(folder_id, output_dir):
    # Query files in the folder
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print("No files found in the folder.")
    else:
        print(f"Downloading {len(files)} files...")
        for file in files:
            file_id = file['id']
            file_name = file['name']
            request = service.files().get_media(fileId=file_id)
            with open(os.path.join(output_dir, file_name), 'wb') as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Downloaded {file_name}: {int(status.progress() * 100)}%")

# Download all files in the folder
folder_id = '1SfJzmq4Nio5MG5fXDtyRfUdn8DKXNtOz'  # Replace with your folder ID
output_dir = 'data'  # Output directory in the repository
os.makedirs(output_dir, exist_ok=True)
download_folder(folder_id, output_dir)
