import folium
import os
import pandas as pd
from UliPlot.XLSX import auto_adjust_xlsx_column_width
import webbrowser


def open_file(f):
    if os.path.isfile(f):
        # absolute path file to open
        my_file = os.path.abspath(f)
        # url file to open
        url = f"file://{my_file}"
        # open file
        webbrowser.open(url,new=1)

# remove file
def remove_file(f):
    if os.path.isfile(f):
        os.remove(f)

# save df in csv file
def save_as_csv(df, f):
    df.to_csv(f, index=False)

# save df in csv file
def save_as_excel(df, f, sheet):
    #df.to_excel(f, sheet_name=sheet, index=False)
    with pd.ExcelWriter(f) as writer:
        df.to_excel(writer, sheet_name=sheet)
        auto_adjust_xlsx_column_width(df, writer, sheet_name=sheet, margin=0)

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
def save_as_map(l_place, l_bike, f):
    # create map
    my_map = create_map(l_place, l_bike)
    # save map
    my_map.save(f)
    # open map
    #############open_file(f)
