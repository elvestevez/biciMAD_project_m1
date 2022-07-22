import random
import os
import pandas as pd
import folium
from UliPlot.XLSX import auto_adjust_xlsx_column_width


path_file = "./data/results/"

# remove file
def remove_file(f):
    if os.path.isfile(f):
        try: 
            os.remove(f)
        except:
            return False
    return f

# name csv file
def get_file_name_csv():
    ran = random.randrange(1000)
    name_f = path_file + "info_" + str(ran) + ".csv"
    return name_f

# name xls file
def get_file_name_excel():
    ran = random.randrange(1000)
    name_f = path_file + "info_" + str(ran) + ".xlsx"
    return name_f

# name html file
def get_file_name_html():
    ran = random.randrange(1000)
    name_f = path_file + "map_" + str(ran) + ".html"
    return name_f

# save df in csv file
def save_as_csv(df):
    # get file name
    f = get_file_name_csv()
    try:
        df.to_csv(f, index=False)
    except:
        return False
    return f

# save df in csv file
def save_as_excel(df):
    # get file name
    f = get_file_name_excel()
    sheet = "bichiMAD"
    #df.to_excel(f, sheet_name=sheet, index=False)
    with pd.ExcelWriter(f) as writer:
        try:
            df.to_excel(writer, sheet_name=sheet)
            # adjust width column to size of content
            auto_adjust_xlsx_column_width(df, writer, sheet_name=sheet, margin=0)
        except:
            return False
    return f

# get zoom
def calculate_zoom(l1, l2):
    dif_lat = abs(l1[0]-l2[0])
    dif_lon = abs(l1[1]-l2[1])
    funct_dif = (dif_lat + dif_lon) / 2 * 1000
    if funct_dif < 1:
        zoom = 17
    elif funct_dif >= 1 and funct_dif < 10:
        zoom = 16
    elif funct_dif >= 10 and funct_dif < 25:
        zoom = 15
    elif funct_dif >= 25 and funct_dif < 50:
        zoom = 14
    elif funct_dif >= 50:
        zoom = 13
    return zoom

# get mid point
def calculate_mid_point(l1, l2):
    loc_mid = []
    # average latitude and longitude
    lat_mid = (l1[0]+l2[0])/2
    lon_mid = (l1[1]+l2[1])/2
    loc_mid.append(lat_mid)
    loc_mid.append(lon_mid)
    return loc_mid

# get mid point and better aprox zoom
def get_point_zoom(loc_1, loc_2):
    point = {}
    # calculate location mid point
    point["location"] = calculate_mid_point(loc_1, loc_2)
    # calculate zoom
    point["zoom"] = calculate_zoom(loc_1, loc_2)
    return point

# create a map with two marked points
def create_map(place, bike):
    # attributes location place
    loc_place = place["location"]
    name_place = place["name"]
    col_place = "red"
    pref_place = "fa"
    icon_place = "info"
    # attributes location bike
    loc_bike = bike["location"]
    name_bike = bike["name"]
    col_bike = "green"
    pref_bike = "fa"
    icon_bike = "bicycle"
    # attribues map
    # calculate mid point and zoom
    mid = get_point_zoom(loc_place, loc_bike)
    # create map mid point
    f_map = folium.Map(location=mid["location"],
                       zoom_start=mid["zoom"])
    # add marks location place and bike
    folium.Marker(loc_place, 
                  tooltip=name_place, 
                  icon=folium.Icon(color=col_place, 
                                   prefix=pref_place, 
                                   icon=icon_place)).add_to(f_map)
    folium.Marker(loc_bike, 
                  tooltip=name_bike, 
                  icon=folium.Icon(color=col_bike, 
                                   prefix=pref_bike, 
                                   icon=icon_bike)).add_to(f_map)
    
    return f_map

# create a map with two marked points
def save_as_map(l_place, l_bike):
    # get file name
    f = get_file_name_html()
    try:
        # create map
        my_map = create_map(l_place, l_bike)
        # save map
        my_map.save(f)
    except:
        return False
    return f
