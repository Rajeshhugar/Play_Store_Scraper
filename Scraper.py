# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:21:32 2024

@author: Rajesh.Hugar
"""

import pandas as pd 
from datetime import datetime
import os 

# Check if directory exists, if not, create it
data_dump_dir = "Data_Dump"
if not os.path.exists(data_dump_dir):
    os.mkdir(data_dump_dir)

os.chdir(data_dump_dir)

from google_play_scraper import Sort, reviews_all

app_id_lst = ["com.spotify.music", "com.jio.media.jiobeats", "com.bsbportal.music"]

for j in range(len(app_id_lst)):
    result_all = []
    for i in range(1, 15):
        result = reviews_all(
            app_id_lst[j],
            sleep_milliseconds=0, # defaults to 0
            lang='en', # defaults to 'en'
            country='in', # defaults to 'us'
            sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT # defaults to None(means all score)
        )
        result_all.extend(result)
    df = pd.DataFrame(result_all)
    
    # Drop duplicates
    df = df.drop_duplicates()
    print(df.shape)
    
    today = str(datetime.now().strftime("%m-%d-%Y_%H%M%S"))
    
    # Save output file with a unique name
    output_file = f'reviews-{app_id_lst[j]}_{today}.xlsx'
    df.to_excel(output_file, index=False)
    print(f"Saved {output_file}")
