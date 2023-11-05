import re
import requests
from scraper_pipeline.custom.scraper.scraper import get_the_fixture_and_results

#define the HEADER so we can escape TRANSFERMARKT's control
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
URL = "https://www.transfermarkt.co.uk/copa-de-la-liga-profesional-de-futbol/gesamtspielplan/wettbewerb/CDLP/saison_id/2022"

@custom
def get_results():
    fixture = get_the_fixture_and_results(header, URL)
    return fixture