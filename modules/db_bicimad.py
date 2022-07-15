import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd
import requests
import os
from dotenv import load_dotenv


# connect DB
def connect_DB():
    load_dotenv('./.env')
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    connectionDB = f'mysql+pymysql://ironhack_user:{DATABASE_PASSWORD}@173.201.189.217/BiciMAD'
    engineDB = create_engine(connectionDB)
    return engineDB

# get data DB
def get_db(engineDB):
    query = '''
    SELECT * 
    FROM bicimad_stations 
    '''
    df =pd.read_sql_query(query, engineDB)
    return df

# get data csv
def get_csv(file):
    df = pd.DataFrame([])
    # if file exists and not empty
    if os.path.isfile(file) and os.path.getsize(file) > 0:
        df = pd.read_csv(file)
    return df

# set longitud and latitud from coordinates
def set_location(df):
    df[['lon_bici','lat_bici']] = df['geometry.coordinates'].str.strip('][').str.split(', ', expand=True)
    return df

# get df bicimad
def get_bicimad_data(origin):
    if origin == "CSV":
        df = get_csv("../datasets/bicimad_stations.csv")
    elif origin == "DB":
        engineMySQL = connect_DB()
        df = get_db(engineMySQL)
    # if df not empty
    if not df.empty:
        df = set_location(df)
    return df
