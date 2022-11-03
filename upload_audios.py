import numpy as np
import pandas as pd
from googleapiclient.http import MediaFileUpload
from Google import Create_Service
def init_drive_service():
    CLIENT_SECRET_FILE='client_secrets.json'
    API_NAME='drive'
    API_VERSION='v3'
    SCOPES=['https://www.googleapis.com/auth/drive']
    service= Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
    return service

def upload_file(path):

    service= init_drive_service()
    media_content= MediaFileUpload(path)
    file_meta_data={
            'name':path.split('/')[-1],
            'parents':'18GgJDkt8wfKUHmXgycbgyNDcIQNQMEZn',
            'stared':False
        }
    file=service.files().create(
        body=file_meta_data,
        media_body=media_content
    ).execute()
    print(file.get("id"))