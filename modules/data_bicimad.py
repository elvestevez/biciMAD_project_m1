import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd
import requests
import os
from dotenv import load_dotenv


BICIMAD_STATIONS_CSV = "../datasets/bicimad_stations.csv"

# connect DB
def connect_DB():
    load_dotenv("./.env")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    # DB mysql
    connectionDB = f"mysql+pymysql://ironhack_user:{DATABASE_PASSWORD}@173.201.189.217/BiciMAD"
    engineDB = create_engine(connectionDB)
    return engineDB

# get data DB
def get_db_stations(engineDB):
    # query bicimad_stations
    query = '''
    SELECT * 
    FROM bicimad_stations 
    '''
    df = pd.read_sql_query(query, engineDB)
    return df

# get data csv
def get_csv_stations(file):
    df = pd.DataFrame([])
    # if file exists and not empty
    if os.path.isfile(file) and os.path.getsize(file) > 0:
        df = pd.read_csv(file)
    return df

# login API EMT and get token
def get_token():
    accessToken = ""
    # get clientid and passkey to connect
    load_dotenv("./.env")
    clientid = os.environ.get("API_CLIENTID")
    passkey = os.environ.get("API_PASSKEY")
    # url and header
    url = "https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/"
    header = {'X-ClientId': clientid,
              'passKey': passkey}
    # call url API get token
    response = requests.get(url, headers=header)
    # if response is ok
    if response.status_code == 200:
        # get token
        response_json = response.json()
        if (response_json["code"] == "01"):
            accessToken = response_json["data"][0]["accessToken"]
    return accessToken
    
# get stations
def get_stations_EMT(token):
    df = pd.DataFrame([])
    # url and header 
    url = "https://openapi.emtmadrid.es/v1/transport/bicimad/stations/"
    header = {'accessToken': token}
    # call url API get stations
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        stations_data = response.json()["data"]
        df = pd.json_normalize(stations_data)
    return df
        
# get data api
def get_api_stations():
    df = pd.DataFrame([])
    # get token
    accessToken = get_token()
    if accessToken != "":
        #get stations
        df = get_stations_EMT(accessToken)
    return df

# get lon list location (first position)
def get_lon(location):
    return location[0]

# get lat list location (second position)
def get_lat(location):
    return location[1]

# set longitud and latitud from coordinates
def set_location(df, origin):
    if origin == "API":
        df["lon_bici"] = df.apply(lambda d: get_lon(d["geometry.coordinates"]), axis=1)
        df["lat_bici"] = df.apply(lambda d: get_lat(d["geometry.coordinates"]), axis=1)
    else:
        df[["lon_bici","lat_bici"]] = df["geometry.coordinates"].str.strip("][").str.split(", ", expand=True)
        df.lon_bici = df.lon_bici.astype(float).fillna(0.0)
        df.lat_bici = df.lat_bici.astype(float).fillna(0.0)
    return df

# get df bicimad
def get_bicimad_data(origin):
    # if origin bicimad is cvs file
    if origin == "CSV":
        df = get_csv_stations(BICIMAD_STATIONS_CSV)
    # if origin bicimad is db
    elif origin == "DB":
        engineMySQL = connect_DB()
        df = get_db_stations(engineMySQL)
    elif origin == "API":
        df = get_api_stations()
    # if df not empty
    if not df.empty:
        df = set_location(df, origin)
    return df

# get filtered bicimad stations take/leave bici and activate/available
def get_filtered_bicimad_data(option):
    # get bicimad 
    # from csv -> at home
    # from DB -> at ironhack
    # from API -> anywhere ¿???
    origin = "API"
    if origin == "CSV":
        print("-------------------------------------------------> vamos por CSV...")
        df = get_bicimad_data("CSV")
    elif origin == "DB":
        print("-------------------------------------------------> vamos por DB...")
        df = get_bicimad_data("DB")
    elif origin == "API":
        print("-------------------------------------------------> vamos por API...")
        df = get_bicimad_data("API")
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
