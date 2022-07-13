from modules import geo_calculations as geo
import pandas as pd


# set distance, add column distance df_bici
def set_distance(df_bici, df_place):
    df_bici['distance'] = df_bici.apply(lambda d: geo.distance_meters(float(d['latitud']), 
                                                                      float(d['longitud']), 
                                                                      df_place["latitude"], 
                                                                      df_place["longitude"]), axis=1 )
    return df_bici

# get bicimad min distance
def get_nearest(df_bici):
    df_result = df_bici[df_bici["distance"] == min(df_bici["distance"])][["name", "address"]]
    return df_result

# get result: selected place + bicimad nearest
def get_bicimad_result(df_place, df_bici):
    # sub df place
    df_place = df_place.reset_index()[["name", "type_place", "address"]].rename(columns={"name": "Place of interest", 
                                                                                         "type_place": "Type of place", 
                                                                                         "address": "Place address"})
    # sub df bicimad
    df_bici = df_bici.reset_index()[["name", "address"]].rename(columns={"name": "BiciMAD station", 
                                                                         "address": "Station location"})
    # join df as result
    df_result = pd.concat([df_place, df_bici], axis=1)
    return df_result

# get BiciMAD nearest from every place
def get_bicimad_nearest(df_place, df_bici):
    df_bicimad_result = pd.DataFrame([])
    # get every place
    for p in range(len(df_place)):
        df_p = pd.DataFrame([df_place.iloc[p]])
        # calculate distance
        df_bici = set_distance(df_bici, df_p)
        # get bicimad nearest
        df_nearest = get_nearest(df_bici)
        # get result, place + bicimad nearest
        df_bicimad_found = get_bicimad_result(df_p, df_nearest)
        # join df results
        df_bicimad_result = pd.concat([df_bicimad_result, df_bicimad_found], axis=0)
    return df_bicimad_result
