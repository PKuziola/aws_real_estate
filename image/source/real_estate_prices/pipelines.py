import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas_gbq

class SaveToGBQPipeline(object):

    def __init__(self):       
        
        json_key_path = os.path.join(os.path.dirname(__file__), '..', 'real-estate-tracker-437718-4857741a8e36.json')
           
        self.credentials = service_account.Credentials.from_service_account_file(
            json_key_path,
            scopes=["https://www.googleapis.com/auth/bigquery"],
        )
        
        self.client = bigquery.Client(
            credentials=self.credentials,
            project=self.credentials.project_id,
        )
        
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):     

        df = pd.DataFrame(self.items)
        df['date'] = pd.to_datetime(df['date'])  

        pandas_gbq.to_gbq(
            df,
            "real-estate-tracker-437718.real_estate_dataset.prices",
            project_id="real-estate-tracker-437718",
            if_exists="append",
            location="US",
            credentials=self.credentials,  # Use the same credentials
        )