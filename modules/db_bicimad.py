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
    # DB mysql
    connectionDB = f'mysql+pymysql://ironhack_user:{DATABASE_PASSWORD}@173.201.189.217/BiciMAD'
    engineDB = create_engine(connectionDB)
    return engineDB

# get data DB
def get_db(engineDB):
    # query bicimad_stations
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
    df.lon_bici = df.lon_bici.astype(float).fillna(0.0)
    df.lat_bici = df.lat_bici.astype(float).fillna(0.0)
    return df

# get df bicimad
def get_bicimad_data(origin):
    # if origin bicimad is cvs file
    if origin == "CSV":
        df = get_csv("../datasets/bicimad_stations.csv")
    # if origin bicimad is db
    elif origin == "DB":
        engineMySQL = connect_DB()
        df = get_db(engineMySQL)
    # if df not empty
    if not df.empty:
        df = set_location(df)
    return df

# get filtered bicimad stations take/leave bici and activate/available
def get_filtered_bicimad_data(option):
    # get bicimad (from csv -> at home, from DB -> at ironhack)
    print("vamos por CSV...")
    df = get_bicimad_data("CSV")
    #print("vamos por DB...")
    #df = get_bicimad_data("DB")
    if not df.empty:
        # if option is take a bike, should be activate and available station and free bikes
        if option == "TAKE":
            mask = (df["activate"] == 1) & (df["no_available"] == 0) & ((df["dock_bikes"] - df["reservations_count"]) > 0)
            df_bici_stations = df[mask]
        # if option is leave a bike, should be activate and available station and free bases
        elif option == "LEAVE":
            mask = (df["activate"] == 1) & (df["no_available"] == 0) & (df["free_bases"] > 0)
            df_bici_stations = df[mask]
        # if no option, should be activate and available station
        else:
            mask = (df["activate"] == 1) & (df["no_available"] == 0)
            df_bici_stations = df[mask]
    else:
        df_bici_stations = pd.DataFrame([])
    return df_bici_stations
