from google.cloud import storage
import pandas as pd

def save_file_to_storage():
    """
    Function to store the newly created parquet files
    into our cloud storage to compose the data lake.
    """
    storage_client = storage.Client()
    bucket_name = 'football_illy'
    blob_name = f"football_db_{pd.to_datetime('today').strftime('YYYY-mm-dd')}"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    with blob.open("w") as f:
        f.write("Test")

save_file_to_storage()