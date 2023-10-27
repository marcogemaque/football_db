import os
import uuid
import psycopg2
import pandas as pd
from dotenv import load_dotenv

def load_credentials():
    """
    A function to load credentials
    from the dotenv.
    """
    load_dotenv("./.secrets/.env")
    username = os.environ["pg_username"]
    password = os.environ["pg_password"]
    database = os.environ["pg_database"]
    host = os.environ["pg_host"]
    return username, password, database, host

def load_team_keys():
    """
    The first function to load teams with the UUIDs
    and the official name.
    """
    #read the file to create the UUIDs
    PATH = "./data/input/team_keys_load.csv"
    df = pd.read_csv(PATH)
    #add UUIDs as a new column to this dataframe
    df["uuid"] = df["country"].apply(lambda x: uuid.uuid4())
    #Get the credentials and add the data to postgres.
    username,password,database,host = load_credentials()
    with psycopg2.connect(user=username,password=password,
        host=host,dbname=database
    ) as conx:
        cursor = conx.cursor()
        #test the connection
        print("testing")
        cursor.execute("SELECT 1")

load_team_keys()