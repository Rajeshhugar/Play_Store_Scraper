import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
from google_play_scraper import Sort, reviews_all
from googleapiclient.http import MediaFileUpload

# Load service account JSON from environment variable
#service_account_info = json.loads(os.environ['SERVICE_ACCOUNT_JSON'])
#service_account_info = os.getenv('SERVICE_ACCOUNT_JSON')

# Define necessary constants
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Load the JSON file
#with open('secret.json', 'r') as f:
 #  content = f.read()
  # print(content)  # Print the content of the file
   #service_account_info = json.loads(content)

# Parse the JSON string into a Python dictionary
#service_account_info = json.loads(service_account_info)

# Authenticate using service account JSON

#credentials = service_account.Credentials.from_service_account_info(service_account_info)


from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
import os
from google_play_scraper import Sort, reviews_all
from googleapiclient.http import MediaFileUpload

# Define necessary constants
#SERVICE_ACCOUNT_FILE = 'service_account.json'
# Load service account JSON from environment variable
#service_account_info = json.loads(os.environ['SERVICE_ACCOUNT_JSON'])
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_IDS = {
  #  "com.jio.media.jiobeats": "1xMbImCG8IXb1uLpZZ01-SgrwHHiqoj86",
  #  "com.spotify.music": "1FYVbhYihhJVjLBbhtHaTaH3WeeSD96GG",
  #  "com.bsbportal.music": "1UrTHLD0tOHQSe7-tO74Ua7CPoWuxqE2E"

 "com.jio.media.jiobeats": "1zHsgD58cZFMuIY4J9jPJjGJpgUnv82Gw",
  "com.spotify.music": "1pNtx0yfKq9Jz0w3TvriSpSB7srzvuEg9",
   "com.bsbportal.music": "1WuFijOR1AhO8gYdTkX-mRR56SIcj7JOe"

 
}

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    #credentials = service_account.Credentials.from_service_account_info(service_account_info,scopes=SCOPES)
    return creds
    #return credentials

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

app_id_lst = ["com.jio.media.jiobeats", "com.spotify.music", "com.bsbportal.music"]

for app_id in app_id_lst:
    result_all = []
    for _ in range(1,5):
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
    folder_id = FOLDER_IDS.get(app_id)


    if folder_id:
        file_name = f'reviews-{app_id}_{today}.parquet'
        file_path = os.path.join('data', file_name)
        
        # Save DataFrame to Parquet
        df.to_parquet(file_path, index=False)
        
        # Example upload_data function (replace with your implementation)
        upload_data(file_path, folder_id)

