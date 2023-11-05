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
#GET THE FIXTURES
fixtures = get_the_fixture_and_results(headers=headers, URL=URL)
#save this file
FILENAME = f"football_db_{pd.to_datetime('today').strftime('YYYY-mm-dd')}"
fixtures.to_csv(f"../data/output/{FILENAME}", index=False)
#and now save this file to storage
save_file_to_storage(bucket_name='football_illy', blob_name=FILENAME)