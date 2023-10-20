import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_squad_overview(headers, URL):
    #make the request
    # URL = "https://www.transfermarkt.co.uk/superliga/startseite/wettbewerb/AR1N"
    page = requests.get(URL, headers=headers)
    #define the soup element to parse the result
    soup = BeautifulSoup(page.content, "html.parser")
    #find the IDs that we're looking for
    results = soup.find(id="yw1", attrs={"class":"grid-view"})
    class_for_table = "items",
    results = results.find_all("table", class_=class_for_table)
    full_table = [x.findChild("tbody") for x in results]
    only_rows = [x.findChildren("td") for x in full_table][0]
    extracted_values = [x.find("a").text if x.find("a") is not None else '' for x in only_rows]
    filtered_values = [x for x in extracted_values if x != ""]
    #now transform it into a dataframe
    club_names = []
    squad_size = []
    squad_value = []
    counter = 0
    for row in filtered_values:
        if counter >= 3:
            counter = 0
        if counter == 0:
            club_names.append(row)
        elif counter == 1:
            squad_size.append(row)
        else:
            squad_value.append(row)
        counter += 1
    df = pd.DataFrame()
    df["club"] = club_names
    df["squad_size"] = squad_size
    df["squad_value"] = squad_value
    return df

def get_the_fixture_and_results(headers, URL):
    #make the request
    # URL = "https://www.transfermarkt.co.uk/professional-football-league/gesamtspielplan/wettbewerb/AR1N/saison_id/2022"
    # URL = "https://www.transfermarkt.co.uk/copa-de-la-liga-profesional-de-futbol/gesamtspielplan/wettbewerb/CDLP/saison_id/2022"
    page = requests.get(URL, headers=headers)
    #define the soup element to parse the result
    soup = BeautifulSoup(page.content, "html.parser")
    #find the IDs that we're looking for
    results = soup.find_all("table")
    all_results_cleaned = pd.DataFrame()
    for mini_table in results:
        td_main_tag = mini_table.find_all("td", class_=[
            "hide-for-small","show-for-small","no-border-rechts",
            "zentriert hauptlink","no-border-links hauptlink"
            ])
        if len(td_main_tag) > 0:
            # extracted_dates = [x.find("a") if x.find("a") != None else "" for x in td_main_tag]
            extracted_time = [x.text if x != None else None for x in td_main_tag]
            #clean the strings
            extracted_time = [re.sub("\s+","",x) for x in extracted_time]
            #now pass it to a dataframe
            df = pd.DataFrame()
            df["match_time"] = extracted_time
            #fillforward the time values
            df["match_time"] = df["match_time"].replace("",pd.NA)
            df = df.dropna()
            df["match_time"] = df["match_time"].ffill()
            df["match_day"] = df["match_time"].apply(lambda x: re.search("[0-9]+/[0-9]+/[0-9][0-9]", x))
            df["match_day"] = df["match_day"].apply(lambda x: x.group() if x != None else None)
            df["drop_day"] = df["match_time"].apply(lambda x: re.search("[a-zA-Z]{3}[0-9]+/[0-9]+/[0-9][0-9]+:", x))
            df["drop_day"] = df["drop_day"].apply(lambda x: x.group() if x != None else None)
            #now we drop the rows for which "drop_day" is filled, because they contain redundant or unlinkable information
            df = df.loc[df["drop_day"].isna()]
            #assign the match_day filled to drop day
            df["drop_day"] = df["match_day"]
            #forward fill the match day
            df["match_day"] = df["match_day"].ffill()
            #drop the rows where DROP_DAY was filled, because they also contain 
            df = df.loc[df["drop_day"].isna()]
            #now drop the column for DROP_DAY
            df = df.drop("drop_day", axis=1)
            df["time_of_match"] = df["match_time"].apply(lambda x: re.search("[0-9][0-9]:[0-9][0-9](P|A)M", x))
            df["time_of_match"] = df["time_of_match"].apply(lambda x: x.group() if x != None else None)
            df["match_time"] = df["match_time"].apply(lambda x: None if re.search("([0-9][0-9]|[0-9]):[0-9][0-9](P|A)M", x) is not None else x)
            df["match_time"] = df["match_time"].fillna("")
            #now extract the match's score
            df["match_score"] = df["match_time"].apply(lambda x: re.search("[0-9]|:[0-9]", x))
            df["match_score"] = df["match_score"].apply(lambda x: x.group() if x != None else None)
            #reset the index
            df = df.reset_index()
            df = df.drop(["index","time_of_match"], axis=1)
            #ignore the "-:-", missing scores, out of our dataframe
            df = df.loc[df["match_time"]!="-:-"]
            #extract the indexes of the values that have a SCORE. The cell BEFORE that is HOME TEAM, the cell after is AWAY TEAM
            indexes_of_score = df["match_score"].loc[df["match_score"].notna()].index.tolist()
            #now access that value to retrieve all the scores. Get the home team, get the away team.
            for index_of_score in indexes_of_score:
                home_team = df.loc[index_of_score-1]["match_time"]
                away_team = df.loc[index_of_score+1]["match_time"]
                df.loc[index_of_score, "home_team"] = home_team
                df.loc[index_of_score, "away_team"] = away_team
            #IF we have HOME_TEAM, that is, a result was extracted, then:
            if "home_team" in df.columns:
                df["home_team"] = df["home_team"].ffill()
                df["away_team"] = df["away_team"].ffill()
                df["match_score"] = df["match_score"].ffill()
                df["home_team"] = df["home_team"].backfill()
                df["away_team"] = df["away_team"].backfill()
                df["match_score"] = df["match_score"].backfill()
                #drop match_time
                df = df.drop("match_time", axis=1)
                df = df.drop_duplicates(subset=["match_score","home_team","away_team"], keep='first')
                #get the goals scored by the home team
                df["goals_home"] = df["match_score"].apply(lambda x: re.search("^[0-9]", x))
                df["goals_home"] = df["goals_home"].apply(lambda x: x.group(0) if x != None else None)
                #get the goals scored by the away team
                df["goals_away"] = df["match_score"].apply(lambda x: re.search("[0-9]$", x))
                df["goals_away"] = df["goals_away"].apply(lambda x: x.group(0) if x != None else None)
                #get the goals scored by the away team
                df["home_team"] = df["home_team"].apply(lambda x: re.sub("\([^()]*\)","", x))
                df["away_team"] = df["away_team"].apply(lambda x: re.sub("\([^()]*\)","", x))
                all_results_cleaned = pd.concat([all_results_cleaned, df])
            #IF we DON'T have that column, it means we will not append this dataframe
            else:
                continue
    return all_results_cleaned

def get_team_stats(headers, URL):
    #make the request
    # URL = "https://www.transfermarkt.co.uk/ca-river-plate/leistungsdaten/verein/209/reldata/%262022/plus/1"
    page = requests.get(URL, headers=headers)
    #define the soup element to parse the result
    soup = BeautifulSoup(page.content, "html.parser")
    #find the IDs that we're looking for
    results = soup.find_all(id="yw1", attrs={"class":"grid-view"})
    results = [x.findChild("table") for x in results]
    results = [x.findChildren("tr") for x in results][0]
    results = [x.find_all("td") for x in results]
    arrays_of_data = []
    for td in results:
        if len(td) > 0:
            #get the position
            _internal_array = []
            for content in td:
                _internal_array.append(content.text)
            if len(_internal_array) > 3:
                arrays_of_data.append(_internal_array)
        else:
            continue
    #after building the array of information, by standard, we can expect the following data:
    squad_status = pd.DataFrame()
    for players_info in arrays_of_data:
        _df_player_stats = pd.DataFrame()
        _df_player_stats["player_number"] = [players_info[0]]
        _df_player_stats["player_name"] = [players_info[3]]
        _df_player_stats["player_position"] = [players_info[4]]
        _df_player_stats["age"] = [players_info[5]]
        _df_player_stats["matches_played"] = [players_info[8]]
        _df_player_stats["goals"] = [players_info[9]]
        _df_player_stats["assists"] = [players_info[10]]
        _df_player_stats["yellow_cards"] = [players_info[11]]
        _df_player_stats["double_yellows"] = [players_info[12]]
        _df_player_stats["red_cards"] = [players_info[13]]
        _df_player_stats["subbed_in"] = [players_info[14]]
        _df_player_stats["subbed_out"] = [players_info[15]]
        _df_player_stats["points_per_game"] = [players_info[16]]
        _df_player_stats["minutes_played"] = [players_info[17]]
        squad_status = pd.concat([squad_status, _df_player_stats])
    squad_status["player_name"] = squad_status["player_name"].str.split(" ")[0]
    squad_status["player_name_fix"] = squad_status["player_name"].apply(lambda x: x[0] + " " + x[-1])
    squad_status["player_name_fix"] = squad_status["player_name_fix"].apply(lambda x: x.split(".")[0] if "." in x else x)
    squad_status["player_name_fix"] = squad_status["player_name_fix"].str.strip()
    squad_status = squad_status.drop("player_name", axis=1)
    #and for the non numeric data in matches_played, change it to 0
    squad_status["matches_played"] = pd.to_numeric(squad_status["matches_played"], errors="coerce")
    #fillna to 0
    squad_status["matches_played"] = squad_status["matches_played"].fillna(0)
    return squad_status