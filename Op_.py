from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
import os
from google_play_scraper import Sort, reviews_all
from googleapiclient.http import MediaFileUpload

# Define necessary constants
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID = '1yaX2B2xNmfUi_qTlmsPqDFHjGeTBf4Xw'  # Update with your parent folder ID

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def create_folder(folder_name):
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)
    
    folder_metadata = {
        'name': folder_name,
        'parents': [PARENT_FOLDER_ID],
        'mimeType': 'application/vnd.google-apps.folder'
    }

    try:
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(f'Folder created: {folder.get("id")}')
        return folder.get('id')
    except Exception as e:
        print('An error occurred while creating the folder:', str(e))
        return None

def upload_data(file_path, folder_id):
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    media_body = MediaFileUpload(file_path)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }

    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media_body,
            fields='id'
        ).execute()

        print('File uploaded:', file.get('id'))
    except Exception as e:
        print('An error occurred while uploading the file:', str(e))


app_id_lst = ["com.spotify.music", "com.jio.media.jiobeats", "com.bsbportal.music"]

for app_id in app_id_lst:
    result_all = []
    
    result = reviews_all(
        app_id,
        sleep_milliseconds=0,
        lang='en',
        country='in',
        sort=Sort.NEWEST
    )
    result_all.extend(result)
    
    df = pd.DataFrame(result_all)
    df = df.drop_duplicates()
    print(df.shape)
    
    today = datetime.now().strftime("%m-%d-%Y_%H%M%S")
    folder_name = f'reviews-{app_id}_{today}'
    folder_id = create_folder(folder_name)
    
    if folder_id:
        file_name = f'{folder_name}.xlsx'
        df.to_excel(file_name, index=False)
        upload_data(file_name, folder_id)



