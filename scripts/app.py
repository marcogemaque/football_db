#internal libs
from time import sleep
import os
import requests
#our created libs
from scraper.scraper import get_the_fixture_and_results
from loader.to_cloud_storage import save_file_to_storage
#third-party
import pandas as pd

#common variables we will use
URL = "https://www.transfermarkt.co.uk/copa-de-la-liga-profesional-de-futbol/gesamtspielplan/wettbewerb/CDLP/saison_id/2022"
#define the HEADER so we can escape TRANSFERMARKT's control
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
#define a variable TODAY to use throughout the code
today = pd.to_datetime('today').strftime('%Y-%m-%d')
#GET THE FIXTURES
print("Scraping for FIXTURES.")
fixtures = get_the_fixture_and_results(headers=headers, URL=URL)
print(f"Succeeded.")
#save this file
FILENAME = f"football_db_{today}.csv"
#and now save this file to storage
save_file_to_storage(bucket_name='football_llyn', file_path_to_upload=FILENAME, object_to_upload=fixtures)