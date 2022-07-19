import time
import pandas as pd
from modules import file_results as res
from modules import email as e
from modules import api_mad as api
from modules import db_bicimad as bic
from modules import geo_calculations as geo


# name result file
name_file_csv = "./results/BiciMAD_nearest.csv"
name_file_excel = "./results/BiciMAD_nearest.xlsx"
name_sheet_excel = "BiciMAD"
name_file_map = "./results/BiciMAD_nearest.html"


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
def export_bicimad_csv(df, f):
    # get and rename columns final result
    df_bicimad_result = get_bicimad_result(df)
    res.save_as_csv(df_bicimad_result, f)
    #print(f"Save results in {f}")
    
# save biciMAD results as csv
def export_bicimad_excel(df, f, sheet):
    # get and rename columns final result
    df_bicimad_result = get_bicimad_result(df)
    res.save_as_excel(df_bicimad_result, f, sheet)
    #print(f"Save results in {f}")

# save biciMAD results as map
def export_bicimad_map(df, f):
    # location 1
    loc_place = {}
    loc_place["location"] = [df.iloc[0]["lat_place"], df.iloc[0]["lon_place"]]
    loc_place["name"] = df.iloc[0]["title"]
    # location 2
    loc_bike = {}
    loc_bike["location"] = [df.iloc[0]["lat_bici"], df.iloc[0]["lon_bici"]]
    loc_bike["name"] = df.iloc[0]["name"]
    # generate map
    res.save_as_map(loc_place, loc_bike, f)
    #print(f"Save results in {f}")

#send excel and map
def send_results_specific_place(df, dir_email):
    # export result as excel
    export_bicimad_excel(df, name_file_excel, name_sheet_excel)
    # export result as map
    export_bicimad_map(df, name_file_map)
    response = e.send_email(dir_email,
                            "Response BiciMAD",
                            """
                            Attachment file results nearest biciMAD.\n
                            Regards,
                            """, 
                            [name_file_map, name_file_excel])
    if response == True:
        print("E-mail sent")
    else:
        print("E-mail couldn't be sent")
    
# send excel
def send_results_every_place(df, dir_email):
    # export result as excel
    export_bicimad_excel(df, name_file_excel, name_sheet_excel)
    response = e.send_email(dir_email,
                            "Response BiciMAD",
                            """
                            Attachment file results nearest biciMAD.\n
                            Regards,
                            """, 
                            [name_file_excel])
    if response == True:
        print("E-mail sent")
    else:
        print("E-mail couldn't be sent")
        
# remove excel and map file
def remove_results_specific_place():
    res.remove_file(name_file_excel)
    res.remove_file(name_file_map)

# remove excel file
def remove_results_every_place():
    res.remove_file(name_file_excel)

# get bicimad min distance
def get_min_distance(df):
    df_result = df.loc[df.groupby('title')['distance'].idxmin()].reset_index(drop=True)
    return df_result

# set distance, add column distance df_bici
def set_distance(df):
    df["distance"] = df.apply(lambda d: geo.distance_meters(d['lat_bici'], 
                                                            d['lon_bici'], 
                                                            d["lat_place"], 
                                                            d["lon_place"]), axis=1)
    return df

# calculate distance between every place from every bicimad
def calculate_distance_bicimad_places(df):
    ###start = time.time()
    # set distance
    df_distance = set_distance(df)
    ###end = time.time()
    ###print(f"calculate_distance_bicimad_places time: {end-start}")    
    return df

# get bicimad and places
def get_bicimad_places(action, interest_place):
    # get places
    df_places = api.get_place_data(interest_place)
    # if places founds
    if not df_places.empty:
        # get bicimad
        df_bicimad = bic.get_filtered_bicimad_data(action)
        if not df_bicimad.empty:
            df_result = df_places.merge(df_bicimad, how='cross')
        else:
            df_result = pd.DataFrame([])
    else:
        df_result = pd.DataFrame([])
    return df_result

# get biciMAD nearest
def get_bicimad_nearest(action, interest_place):
    # get bicimad and places (selected or every place)
    df_bicimad_places = get_bicimad_places(action, interest_place)
    # if bicimad and places are found
    if not df_bicimad_places.empty:
        print("Searching...")
        # calculate distance for every place and all bicimad stations
        df_bicimad_distance = calculate_distance_bicimad_places(df_bicimad_places)
        # get place and bicimad min distance
        df_bicimad_nearest = get_min_distance(df_bicimad_distance)
    else:
        df_bicimad_nearest = pd.DataFrame([])
    return df_bicimad_nearest

# get biciMAD for every place
def every_place_bicimad(action, email):
    # remove old results
    remove_results_every_place()    
    # get bicimad nearest
    df_result = get_bicimad_nearest(action, "")
    if not df_result.empty:
        # send results
        send_results_every_place(df_result, email)

# get biciMAD for specific place
def specific_place_bicimad(action, interest_place, email):
    # remove old results
    remove_results_specific_place()    
    # get bicimad nearest
    df_result = get_bicimad_nearest(action, interest_place)
    if not df_result.empty:
        # send results
        send_results_specific_place(df_result, email)
