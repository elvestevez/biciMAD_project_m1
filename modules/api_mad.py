import requests
import json
import pandas as pd

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
def set_selected_place(place):
    place_json = {}
    # get name 
    place_json["name"] = place["title"]
    # get type_place 
    place_json["type_place"] = place["type_place"]
    # get address 
    place_json["address"] = place["address"]["street-address"]
    # get latitude place 
    place_json["latitude"] = place["location"]["latitude"]
    # get longitude place 
    place_json["longitude"] = place["location"]["longitude"]
    return place_json

# get place for name. 
# if name is empty, return all places
# if name isn't empty, return places found for this name
def get_place(name, data):
    if name == "":
        # get all places
        list_json = [set_selected_place(d) for d in data]
        # create cleaned dataframe for places
        df = pd.DataFrame(list_json)
    else:
        # get place found 
        place_list = [d for d in data if d["title"].upper() == name.upper()]
        if len(place_list) == 0:
            df = pd.DataFrame([])
        else:
            list_json = [set_selected_place(d) for d in place_list]
            # create cleaned dataframe for places found
            df = pd.DataFrame(list_json)
    return df
