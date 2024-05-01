
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd 
from datetime import datetime
import os 
from google_play_scraper import Sort, reviews_all
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# Define necessary constants
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID = '1yaX2B2xNmfUi_qTlmsPqDFHjGeTBf4Xw'  # Update with your parent folder ID

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_data(file_path):
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

  
    media_body = MediaFileUpload(file_path)  # Import MediaFileUpload from googleapiclient.http

    file = service.files().create(
        media_body=media_body,
        fields='id'
    ).execute()

    print('File uploaded:', file.get('id'))

data_dump_dir = "data"
if not os.path.exists(data_dump_dir):
    os.mkdir(data_dump_dir)

os.chdir(data_dump_dir)

from google_play_scraper import Sort, reviews_all
app_id_lst= ["com.spotify.music","com.jio.media.jiobeats","com.bsbportal.music"]

for j in range(len(app_id_lst)):
    result_all = []
    for i in range(1,15):
        result = reviews_all(
            app_id_lst[j],
            sleep_milliseconds=0, # defaults to 0
            lang='en', # defaults to 'en'
            country='in', # defaults to 'us'
            sort= Sort.NEWEST, # defaults to Sort.MOST_RELEVANT # defaults to None(means all score)
        )
    
        result_all.extend(result)
    df = pd.DataFrame(result_all)
    

    df = df.drop_duplicates()
    print(df.shape)
    today = str(datetime.now().strftime("%m-%d-%Y_%H%M%S"))
    file_name = f'reviews-{app_id_lst[j]}_{today}.xlsx'
    df.to_excel(file_name,index=False)

    upload_data(file_name)

    