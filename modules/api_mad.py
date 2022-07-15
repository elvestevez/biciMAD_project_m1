import requests
import json
import pandas as pd
from modules import match_place as match


DATASET_CULTURAL = "https://datos.madrid.es/egob/catalogo/200304-0-centros-culturales.json"
DATASET_MUSEUM = "https://datos.madrid.es/egob/catalogo/201132-0-museos.json"


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
    return ds

# create df selected place 
def set_element_place(place):
    place_json = {}
    # get name 
    place_json["title"] = place["title"]
    # get type_place 
    place_json["type_place"] = place["type_place"]
    # get address 
    place_json["address_place"] = place["address"]["street-address"]
    # get latitude place 
    place_json["lat_place"] = place["location"]["latitude"]
    # get longitude place 
    place_json["lon_place"] = place["location"]["longitude"]
    return place_json

# get places data
def get_places_data():
    # load datasets
    places_dataset = load_datasets()
    # create cleaned dataframe for places
    list_json = [set_element_place(d) for d in places_dataset]
    df = pd.DataFrame(list_json)
    return df

# get place by name (the best match aprox)
def get_place_by_name(name, df):
    df_selected = match.get_match(name, "title", df)
    return df_selected
