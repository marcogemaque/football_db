import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

load_dotenv(".secrets/.env")

def connect_to_db():
    """
    A function to connect to the database.Returns a driver and cursor.

    Parameters
    -------------

    Returns
    -------------
    connection
        psycopg2.connect
    cursor
        psycopg2.cursor
    """
    server:str = os.environ["server"]
    user:str = os.environ["user"]
    password:str = os.environ["password"]
    db:str = os.environ["db"]
    connection = psycopg2.connect(
        host=server, dbname=db,
        user=user,password=password)
    cursor = connection.cursor()
    return connection, cursor

def query_team_urls():
    """
    Queries the URLS to search for each team (with UUID).
    """
    connection, cursor = connect_to_db()
    query = "SELECT * FROM football_dwh.scrape_urls left join football_dwh.team_keys using(uuid);"
    team_urls_to_query = pd.read_sql_query(query, con=connection)
    return team_urls_to_query

def delete_all_data_from_table(table_name:str):
    """
    A function to delete ALL ROWS from table_name.
    """
    connection, cursor = connect_to_db()
    query = f"delete from football_dwh.{table_name}"
    cursor.execute(query)