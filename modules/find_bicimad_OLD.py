import time
import pandas as pd
from modules import api_mad as api
from modules import db_bicimad as bic
from modules import geo_calculations as geo
from modules import export_results as exp


# name result file
file_csv = "./results/BiciMAD_nearest.csv"
file_map = "./results/BiciMAD_nearest.html"


# set distance, add column distance df_bici
def set_distance(df_b, df_p):
    df_b["distance"] = df_b.apply(lambda d: geo.distance_meters(float(d['lat_bici']), 
                                                                float(d['lon_bici']), 
                                                                df_p["lat_place"], 
                                                                df_p["lon_place"]), axis=1 )
    return df_b

# get bicimad min distance
def get_min_distance(df_bici):
    df_result = df_bici[df_bici["distance"] == df_bici["distance"].min()][["name", "address", "lon_bici", "lat_bici"]]
    return df_result

# filter df take/leave bici
def filter_df_bicimad(df, option):
    # if option is take a bike, should be activate and available station and free bikes
    if option == "TAKE":
        mask = (df["activate"] == 1) & (df["no_available"] == 0) & ((df["dock_bikes"] - df["reservations_count"]) > 0)
        df_filtered = df[mask]
    # if option is leave a bike, should be activate and available station and free bases
    elif option == "LEAVE":
        mask = (df["activate"] == 1) & (df["no_available"] == 0) & (df["free_bases"] > 0)
        df_filtered = df[mask]
    # if no option, should be activate and available station
    else:
        mask = (df["activate"] == 1) & (df["no_available"] == 0)
        df_filtered = df[mask]
    return df_filtered
    
# get result: clean columns
def get_bicimad_result(df):
    # rename
    df_bici_result = df[["title", 
                         "type_place", 
                         "address", 
                         "name", 
                         "address"]].rename(columns={"title": "Place of interest",
                                                     "type_place": "Type of place", 
                                                     "address_place": "Place address",
                                                     "name": "BiciMAD station",
                                                     "address": "Station location"})
    return df_bici_result

# get result: selected place + bicimad nearest
def get_result(df_place, df_bici):
    # sub df place
    df_place = df_place.reset_index()
    # sub df bicimad
    df_bici = df_bici.reset_index()
    # join df as result
    df_result = pd.concat([df_place, df_bici], axis=1)
    return df_result

# get nearest from every place
def get_nearest(df_place, df_bici, bike):
    # filter bike stations activate, available
    df_bici_available = filter_df_bicimad(df_bici, bike)
    #df_bici_available = df_bici
    # get every place
    df_result = pd.DataFrame([])
    for p in range(len(df_place)):
        df_p = pd.DataFrame([df_place.iloc[p]])
        # calculate distance
        df_bici_available = set_distance(df_bici_available, df_p)
        # get bicimad min distance
        df_nearest = get_min_distance(df_bici_available)
        # get result, place + bicimad nearest
        df_bicimad_found = get_result(df_p, df_nearest)
        # join df results
        df_result = pd.concat([df_result, df_bicimad_found], axis=0)
    return df_result

# get biciMAD nearest
def get_bicimad_nearest(interest_place, bike):
    # create empty df as results
    df_result = pd.DataFrame([])
    
    # get places
    start = time.time()
    df_places = api.get_places_data()
    end = time.time()
    print(f"Process get places: {end-start}")    
    
    # if interest_place has info, find a place
    start = time.time()
    if interest_place != "":
        # get place by name
        df_my_place = api.get_place_by_name(interest_place, df_places)
        # if place not found, return empty result
        if not df_my_place.empty:
            matched_name = df_my_place.iloc[0]["title"]
            print(f"Matched interest place: {matched_name}")
    else:
        df_my_place = df_places
    
    end = time.time()
    print(f"Process get specific place: {end-start}")
    
    print(f"Search in process...")
    
    # get bicimad (from csv -> at home, from DB -> at ironhack)
    print("vamos por CSV...")
    df_bicimad = bic.get_bicimad_data("CSV")
    #print("vamos por DB...")
    #df_bicimad = bic.get_bicimad_data("DB")
    if not df_bicimad.empty:
        ########## TODOOOOOOOOOO
        #df_my_place = df_my_place[:6]
        #print("testing only for 6 first")
        ##########
        # get bicimad nearest for every place found
        start = time.time()
        df_result = get_nearest(df_my_place, df_bicimad, bike)
        end = time.time()
        print(f"Process calculate distance min: {end-start}")
    
    else:
        print(f"BiciMAD data not found")
    
    return df_result

# save biciMAD results as csv
def save_bicimad_csv(df):
    df_bicimad_result = get_bicimad_result(df)
    exp.export_csv(df_bicimad_result, file_csv)
    print(f"Save results in {file_csv}")

# save biciMAD results as map
def save_bicimad_map(df):
    def_map = {}
    # attributes location 1
    def_map["location1"] = [df["lat_place"], df["lon_place"]]
    def_map["title1"] = df.iloc[0]["title"]
    def_map["color1"] = "red"
    def_map["pref1"] = "fa"
    def_map["icon1"] = "info"
    # attributes location 2
    def_map["location2"] = [df["lat_bici"], df["lon_bici"]]
    def_map["title2"] = df.iloc[0]["name"]
    def_map["color2"] = "green"
    def_map["pref2"] = "fa"
    def_map["icon2"] = "bicycle"
    # attribues map
    def_map["zoom"] = 13
    exp.export_map(def_map, file_map)
    print(f"Save results in {file_map}")

# get biciMAD for every place
def every_place_bicimad(bike):
    # remove results file, if exists
    exp.remove_file(file_csv)    
    # get bicimad nearest
    df_result = get_bicimad_nearest("", bike)
    if not df_result.empty:
        # save result as csv
        start = time.time()
        save_bicimad_csv(df_result)
        end = time.time()
        print(f"Process save file: {end-start}")

# get biciMAD for specific place
def specific_place_bicimad(interest_place, bike):
    # remove results map, if exists
    exp.remove_file(file_map)    
    # get bicimad nearest
    df_result = get_bicimad_nearest(interest_place, bike)
    if not df_result.empty:
        #print(df_result)
        # save result as map
        start = time.time()
        save_bicimad_map(df_result)
        end = time.time()
        print(f"Process save map: {end-start}")
        # save result as csv
        start = time.time()
        save_bicimad_csv(df_result)
        end = time.time()
        print(f"Process save file: {end-start}")

# get biciMAD for every place to take a bike
def every_place_take_bicimad():
    start = time.time()
    bike = "TAKE"
    every_place_bicimad(bike)
    end = time.time()
    print(f"Process every_place_take_bicimad: {end-start}")

# get biciMAD for every place to leave a bike
def every_place_leave_bicimad():
    start = time.time()
    bike = "LEAVE"
    every_place_bicimad(bike)
    end = time.time()
    print(f"Process every_place_leave_bicimad: {end-start}")

# get biciMAD for specific place to take a bike
def specific_place_take_bicimad(interest_place):
    start = time.time()
    bike = "TAKE"
    specific_place_bicimad(interest_place, bike)
    end = time.time()
    print(f"Process specific_place_take_bicimad: {end-start}")

# get biciMAD for specific place to leave a bike
def specific_place_leave_bicimad(interest_place):
    start = time.time()
    bike = "LEAVE"
    specific_place_bicimad(interest_place, bike)
    end = time.time()
    print(f"Process specific_place_leave_bicimad: {end-start}")
