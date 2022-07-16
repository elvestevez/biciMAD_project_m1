import requests
import json
import pandas as pd
from modules import match_place as match


DATASET_CULTURAL = "https://datos.madrid.es/egob/catalogo/200304-0-centros-culturales.json"
DATASET_MUSEUM = "https://datos.madrid.es/egob/catalogo/201132-0-museos.json"
#DATASET_PARKS = "https://datos.madrid.es/egob/catalogo/200761-0-parques-jardines.json"


# get dataset from URL API Ayuntamiento Madrid
def get_dataset(url, type_ds):
    # get response of url and convert to json
    response = requests.get(url)
    dataset_json = response.json()
    dataset = [dict(d, type_place=type_ds) for d in [dat for dat in dataset_json["@graph"]]]
    return dataset

# join two datasets (both are list of json)
def join_datasets(dt1, dt2):
    # join datasets (list of dict)
    dt_join = dt1 + dt2
    return dt_join

# load selected datasets
def load_datasets():
    ds = join_datasets(get_dataset(DATASET_CULTURAL, "Centros Culturales Municipales (incluyen Socioculturales y Juveniles)"), 
                       get_dataset(DATASET_MUSEUM, "Museos de la ciudad de Madrid"))
    #ds = get_dataset(DATASET_PARKS, "parques y jardines")
    return ds

# get places data
def get_places_data():
    # load datasets
    places_dataset = load_datasets()
    df = pd.json_normalize(places_dataset)[["title", 
                                            "type_place", 
                                            "address.street-address", 
                                            "location.latitude", 
                                            "location.longitude"]].rename(columns={"address.street-address": "address_place",
                                                                                   "location.latitude": "lat_place",
                                                                                   "location.longitude": "lon_place"})
    df = df.dropna()
    return df

# get place by name (the best match aprox)
def get_place_by_name(name, df):
    df_selected = match.get_match(name, "title", df)
    return df_selected
