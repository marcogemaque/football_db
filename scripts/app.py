#internal libs
from time import sleep
import os
import requests
#our created libs
from scraper.scraper import get_the_fixture_and_results

#common variables we will use
URL = "https://www.transfermarkt.co.uk/copa-de-la-liga-profesional-de-futbol/gesamtspielplan/wettbewerb/CDLP/saison_id/2022"
#define the HEADER so we can escape TRANSFERMARKT's control
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
#GET THE FIXTURES
fixtures = get_the_fixture_and_results(headers=headers, URL=URL)
print(fixtures.head(3))