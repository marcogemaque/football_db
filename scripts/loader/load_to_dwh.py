from api import delete_all_data_from_table
from google.cloud import storage
import pandas as pd

def load_team_stats(bucket_name:str, name_of_file):
    """
    Function to load to table TEAM_STATS today's file.
    """
    #delete all the player's data from the table
    delete_all_data_from_table("player_stats")
    #now read the data from the data lake
    storage_client = storage.Client.from_service_account_json("./.secrets/fifa-project-399416-df12ebf73aeb.json")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(name_of_file)
    blob.download_to_filename(f"./data/output/{name_of_file}")
    #now read that file and load it to the actual 
    df_to_load = pd.read_csv(f"./data/output/{name_of_file}")