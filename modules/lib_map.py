import folium
import os


def remove_map(f):
    if os.path.isfile(f):
        os.remove(f)

# create a map with two marked points
def create_map(json):
    # attributes location 1
    loc1 = json["location1"]
    tit1 = json["title1"]
    col1 = json["color1"]
    pref1 = json["pref1"]
    icon1 = json["icon1"]
    # attributes location 2
    loc2 = json["location2"]
    tit2 = json["title2"]
    col2 = json["color2"]
    pref2 = json["pref2"]
    icon2 = json["icon2"]
    # attribues map
    zoom = json["zoom"]

    # create map location1
    f_map = folium.Map(location=loc1,
                       zoom_start=zoom)
    # add marks location 1 and 2
    folium.Marker(loc1, tooltip=tit1, icon=folium.Icon(color=col1, prefix=pref1, icon=icon1)).add_to(f_map)
    folium.Marker(loc2, tooltip=tit2, icon=folium.Icon(color=col2, prefix=pref2, icon=icon2)).add_to(f_map)
    
    return f_map

# create a map with two marked points
def generate_map(json_map, f):
    my_map = create_map(json_map)
    my_map.save(f)
