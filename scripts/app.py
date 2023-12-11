#internal libs
from time import sleep
import os
#our created libs
from scraper.scraper import get_the_fixture_and_results, get_team_stats
from loader.to_cloud_storage import save_file_to_storage
from loader.load_to_dwh import load_file_to_table
from api import query_team_urls, query_team_aliases
#third-party
import pandas as pd
import requests

def apply_aliases_to_uuid(row, df_with_aliases):
    """
    Pandas Apply function to look for the aliases, see if there's a match,
    if there is, get the UUID
    """
    team_uuids = df_with_aliases["uuid"].tolist()
    team_aliases = df_with_aliases["alias"].tolist()
    print(team_aliases)
    return row

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
FILENAME = f"FIXTURES|football-db|{today}.csv"
#and now save this file to storage
save_file_to_storage(bucket_name='football_llyn', file_path_to_upload=FILENAME, object_to_upload=fixtures)
##################
#SAVE THE FIXTURE
##################
#first of all query the team's aliases
teams_aliases = query_team_aliases()
#iterate over the UUIDs, get the possible aliases and see if there's a match.
teams_aliases = teams_aliases.apply(apply_aliases_to_uuid, axis=1, args=(teams_aliases,))
print(f"Saving the FIXTURE of TODAY...")
FILENAME = f"FIXTURES|football-db|{today}.csv"
load_file_to_table(bucket_name='football_llyn', name_of_file=FILENAME, 
                   table_name="matches_played", drop_columns=True, cols_to_drop=["match_score"])
print("Succeeded.")
#get URLs to scrape for the TEAM STATS
teams_urls_to_scrape = query_team_urls()
uuid = teams_urls_to_scrape["uuid"].tolist()
team_name = teams_urls_to_scrape["team_name"].tolist()
url_scrape = teams_urls_to_scrape["url"].tolist()
all_team_stats = pd.DataFrame()
for url in url_scrape:
    print("Scraping for TEAM STATS.")
    team_stat = get_team_stats(headers=headers, URL=url)
    team_stat["uuid"] = uuid[url_scrape.index(url)]
    team_stat["team_name"] = team_name[url_scrape.index(url)]
    all_team_stats = pd.concat([all_team_stats, team_stat])
    print(f"Succeeded.")
FILENAME = f"TEAM-STATS|football-db|{today}.csv"
save_file_to_storage(bucket_name='football_llyn', file_path_to_upload=FILENAME, object_to_upload=all_team_stats)
##################
#SAVE THE TEAM STATS
##################
print(f"Saving the TEAM STATS of TODAY...")
load_file_to_table(bucket_name='football_llyn', name_of_file=FILENAME, 
                   table_name="team_stats", drop_columns=True, cols_to_drop=["team_name"])
print("Succeeded.")