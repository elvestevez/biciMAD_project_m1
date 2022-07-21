import time
import random
import pandas as pd
from modules import file_results as res
from modules import to_email as email
from modules import data_mad as api
from modules import data_bicimad as bic
from modules import geo_calculations as geo


# remove reports 
def remove_results(reports):
    if len(reports) > 0:
        for filename in reports:
            print(f"-----------------------------------> borrando {filename}")
            res.remove_file(filename)

#send reports
def send_results(reports, dir_email):
    subject_text = "Reports bichiMAD"
    body_text = """
                Hi,\n
                Attachment file results with nearest bike station.\n\n
                Regards,
                """
    response = email.send_email(dir_email,
                                subject_text,
                                body_text, 
                                reports)
    if response == True:
        print("\nE-mail sent")
    else:
        print("\nE-mail couldn't be sent")

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
def export_bicimad_csv(df):
    # get and rename columns final result
    df_bicimad_result = get_bicimad_result(df)
    f = res.save_as_csv(df_bicimad_result)
    return f

# save biciMAD results as csv
def export_bicimad_excel(df):
    # get and rename columns final result
    df_bicimad_result = get_bicimad_result(df)
    f = res.save_as_excel(df_bicimad_result)
    return f

# save biciMAD results as map
def export_bicimad_map(df):
    # location 1
    loc_place = {}
    loc_place["location"] = [df.iloc[0]["lat_place"], df.iloc[0]["lon_place"]]
    loc_place["name"] = df.iloc[0]["title"]
    # location 2
    loc_bike = {}
    loc_bike["location"] = [df.iloc[0]["lat_bici"], df.iloc[0]["lon_bici"]]
    loc_bike["name"] = df.iloc[0]["name"]
    # generate map
    f = res.save_as_map(loc_place, loc_bike)
    return f

#send excel and map
def send_results_specific_place(df, dir_email):
    # export result as excel
    f_xlsx = export_bicimad_excel(df)
    # export result as map
    f_html = export_bicimad_map(df)
    # list of reports
    reports = [f_xlsx, f_html]
    # send email
    send_results(reports, dir_email)
    # remove files after send
    ######remove_results(reports)
    
# send excel
def send_results_every_place(df, dir_email):
    # export result as excel
    f_xlsx = export_bicimad_excel(df)
    # list of reports
    reports = [f_xlsx]
    # send email
    send_results(reports, dir_email)
    # remove files after send
    ######remove_results(reports)
    
# get bicimad min distance
def get_min_distance(df):
    df_result = df.loc[df.groupby("title")["distance"].idxmin()].reset_index(drop=True)
    return df_result

# set distance, add column distance df_bici
def set_distance(df):
    df["distance"] = df.apply(lambda d: geo.distance_meters(d["lat_bici"], 
                                                            d["lon_bici"], 
                                                            d["lat_place"], 
                                                            d["lon_place"]), axis=1)
    return df

# calculate distance between every place from every bicimad
def calculate_distance_bicimad_places(df):
    ###start = time.time()
    # set distance
    df_distance = set_distance(df)
    ###end = time.time()
    ###print(f"-------------> calculate_distance_bicimad_places time: {end-start}")    
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
        print("\nSearching...")
        # calculate distance for every place and all bicimad stations
        df_bicimad_distance = calculate_distance_bicimad_places(df_bicimad_places)
        # get place and bicimad min distance
        df_bicimad_nearest = get_min_distance(df_bicimad_distance)
    else:
        df_bicimad_nearest = pd.DataFrame([])
    return df_bicimad_nearest

# get biciMAD for every place
def every_place_bicimad(action, email):
    # get bicimad nearest
    df_result = get_bicimad_nearest(action, "")
    if not df_result.empty:
        # send results
        send_results_every_place(df_result, email)

# get biciMAD for specific place
def specific_place_bicimad(action, interest_place, email):
    # get bicimad nearest
    df_result = get_bicimad_nearest(action, interest_place)
    if not df_result.empty:
        # send results
        send_results_specific_place(df_result, email)
