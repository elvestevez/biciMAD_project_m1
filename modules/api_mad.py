import requests
import json
import pandas as pd
from modules import match_place as match


DATASET_CULTURAL = "https://datos.madrid.es/egob/catalogo/200304-0-centros-culturales.json" # "Centros Culturales Municipales (incluyen Socioculturales y Juveniles)"
DATASET_MUSEUM = "https://datos.madrid.es/egob/catalogo/201132-0-museos.json" # "Museos de la ciudad de Madrid"
DATASET_PARKS = "https://datos.madrid.es/egob/catalogo/200761-0-parques-jardines.json" # "Principales parques y jardines municipales"


# get dataset from URL API Ayuntamiento Madrid
def get_dataset(url, type_ds):
    # get response of url and convert to json
    response = requests.get(url)
    dataset_json = response.json()
    dataset = [dict(d, type_place=type_ds) for d in [dat for dat in dataset_json["@graph"]]]
    return dataset

# join n datasets
def join_datasets(*args):
    # join datasets (list of dict)
    dt_join = []
    for d in args:
        dt_join += d
    return dt_join

# load selected datasets
def load_datasets():
    # get and join datasets
    ds = join_datasets(get_dataset(DATASET_CULTURAL, "Centros Culturales Municipales (incluyen Socioculturales y Juveniles)"), 
                       get_dataset(DATASET_MUSEUM, "Museos de la ciudad de Madrid"))
    return ds

# get places data
def get_all_places():
    # load datasets
    places_dataset = load_datasets()
    # normalize and get needed columns
    df = pd.json_normalize(places_dataset)[["title", 
                                            "type_place", 
                                            "address.street-address", 
                                            "location.latitude", 
                                            "location.longitude"]].rename(columns={"address.street-address": "address_place",
                                                                                   "location.latitude": "lat_place",
                                                                                   "location.longitude": "lon_place"})
    # remove rows with NA values
    df = df.dropna()
    return df

# get place data
# if name_place is empty, return all places
# if name_place isn't empty, return place match by name (the best match aprox)
def get_place_data(name_place):
    # get every place
    df_all_places = get_all_places()
    # check if df places is not empty
    if not df_all_places.empty:
        # if name_place is not empty, find place by name
        if name_place != "":
            # get place by name
            df_selected = match.get_match(name_place, "title", df_all_places)
            # if place not found, return empty result
            if not df_selected.empty:
                df_my_place = df_selected
                # print found place
                matched_name = df_selected.iloc[0]["title"]
                print(f"Matched interest place: {matched_name}")
            else:
                df_my_place = pd.DataFrame([])
        # if name_place is empty, return all places
        else:
            df_my_place = df_all_places
    else:
        df_my_place = pd.DataFrame([])

    return df_my_place
