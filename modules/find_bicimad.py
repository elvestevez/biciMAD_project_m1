import time
import pandas as pd
from modules import results as res
from modules import api_mad as api
from modules import db_bicimad as bic
from modules import geo_calculations as geo


# name result file
file_csv = "./results/BiciMAD_nearest.csv"
file_excel = "./results/BiciMAD_nearest.xlsx"
name_sheet = "BiciMAD"
file_map = "./results/BiciMAD_nearest.html"


# get clean result to export
def get_bicimad_result(df):
    # select and rename columns
    df_bici_result = df[["title", 
                         "type_place", 
                         "address_place", 
                         "name", 
                         "address"]].rename(columns={"title": "Place of interest",
                                                     "type_place": "Type of place", 
                                                     "address_place": "Place address",
                                                     "name": "BiciMAD station",
                                                     "address": "Station location"})
    return df_bici_result

# save biciMAD results as csv
def save_bicimad_csv(df):
    # get and rename columns final result
    df_bicimad_result = get_bicimad_result(df)
    res.export_csv(df_bicimad_result, file_csv)
    print(f"Save results in {file_csv}")
    
# save biciMAD results as csv
def save_bicimad_excel(df):
    # get and rename columns final result
    df_bicimad_result = get_bicimad_result(df)
    res.export_excel(df_bicimad_result, file_excel, name_sheet)
    print(f"Save results in {file_excel}")    

# save biciMAD results as map
def save_bicimad_map(df):
    # location 1
    loc_place = {}
    loc_place["location"] = [df.iloc[0]["lat_place"], df.iloc[0]["lon_place"]]
    loc_place["name"] = df.iloc[0]["title"]
    # location 2
    loc_bike = {}
    loc_bike["location"] = [df.iloc[0]["lat_bici"], df.iloc[0]["lon_bici"]]
    loc_bike["name"] = df.iloc[0]["name"]
    # generate map
    res.export_map(loc_place, loc_bike, file_map)
    print(f"Save results in {file_map}")

# get bicimad min distance
def get_min_distance(df):
    df_result = df.loc[df.groupby('title')['distance'].idxmin()]
    return df_result

# set distance, add column distance df_bici
def set_distance(df):
    df["distance"] = df.apply(lambda d: geo.distance_meters(d['lat_bici'], 
                                                            d['lon_bici'], 
                                                            d["lat_place"], 
                                                            d["lon_place"]), axis=1 )
    return df

# calculate distance between every place from every bicimad
def calculate_distance_bicimad_places(df):
    start = time.time()
    # set distance
    df_distance = set_distance(df)
    end = time.time()
    print(f"calculate_distance_bicimad_places time: {end-start}")    
    return df

# get bicimad and places
def get_bicimad_places(interest_place, action):
    # get places
    df_places = api.get_place_data(interest_place)
    # get bicimad
    df_bicimad = bic.get_filtered_bicimad_data(action)
    # merge df, if both not empty
    if not df_bicimad.empty and not df_places.empty:
        df_result = df_places.merge(df_bicimad, how='cross')
    else:
        df_result = pd.DataFrame([])
    return df_result

# get biciMAD nearest
def get_bicimad_nearest(interest_place, action):
    # get bicimad and places (selected or every place)
    df_bicimad_places = get_bicimad_places(interest_place, action)
    # calculate distance for every place and all bicimad stations
    df_bicimad_distance = calculate_distance_bicimad_places(df_bicimad_places)
    # get place and bicimad min distance
    df_bicimad_nearest = get_min_distance(df_bicimad_distance)
    return df_bicimad_nearest

# get biciMAD for every place
def every_place_bicimad(action):
    # remove results file, if exists
    res.remove_file(file_excel)
    
    # get bicimad nearest
    df_result = get_bicimad_nearest("", action)
    if not df_result.empty:
        # save result as csv
        save_bicimad_excel(df_result)

# get biciMAD for specific place
def specific_place_bicimad(interest_place, action):
    # remove results file and map, if exists
    res.remove_file(file_excel)
    res.remove_file(file_map)
    
    # get bicimad nearest
    df_result = get_bicimad_nearest(interest_place, action)
    if not df_result.empty:
        #print(df_result)
        # save result as csv
        save_bicimad_excel(df_result)
        # save result as map
        save_bicimad_map(df_result)

# get biciMAD for every place to take a bike
def every_place_take_bicimad():
    start = time.time()
    action_bike = "TAKE"
    every_place_bicimad(action_bike)
    end = time.time()
    print(f"every_place_take_bicimad time: {end-start}")

# get biciMAD for every place to leave a bike
def every_place_leave_bicimad():
    start = time.time()
    action = "LEAVE"
    every_place_bicimad(action)
    end = time.time()
    print(f"every_place_leave_bicimad time: {end-start}")

# get biciMAD for specific place to take a bike
def specific_place_take_bicimad(interest_place):
    start = time.time()
    action_bike = "TAKE"
    specific_place_bicimad(interest_place, action_bike)
    end = time.time()
    print(f"specific_place_take_bicimad time: {end-start}")

# get biciMAD for specific place to leave a bike
def specific_place_leave_bicimad(interest_place):
    start = time.time()
    action_bike = "LEAVE"
    specific_place_bicimad(interest_place, action_bike)
    end = time.time()
    print(f"specific_place_leave_bicimad time: {end-start}")
