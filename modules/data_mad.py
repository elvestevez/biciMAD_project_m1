import requests
import json
import pandas as pd
from modules import match_place as match


DATASETS = [{"url": "https://datos.madrid.es/egob/catalogo/200304-0-centros-culturales.json", 
             "type_ds": "Centros Culturales Municipales (incluyen Socioculturales y Juveniles)"},
            {"url": "https://datos.madrid.es/egob/catalogo/201132-0-museos.json",
             "type_ds": "Museos de la ciudad de Madrid"}]

# get dataset from URL API Ayuntamiento Madrid
def get_dataset(datas):
    dt_join = []
    # get every dataset 
    if len(datas) > 0:   
        for dict_ds in datas:
            # get response of url and convert to json
            response = requests.get(dict_ds["url"])
            dataset_json = response.json()
            dataset = [dict(d, type_place=dict_ds["type_ds"]) for d in [dat for dat in dataset_json["@graph"]]]
            #join dataset
            dt_join += dataset
    return dt_join

# load selected datasets
def load_datasets():
    # get and join datasets
    ds = get_dataset(DATASETS)
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
                print(f"\nMatched interest place: {matched_name}")
            else:
                df_my_place = pd.DataFrame([])
                print(f"\nNot found interest place: {name_place}")
        # if name_place is empty, return all places
        else:
            df_my_place = df_all_places
    else:
        df_my_place = pd.DataFrame([])

    return df_my_place
