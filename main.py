from modules import api_mad as api
from modules import db_bicimad as bic
from modules import find_bicimad as find
import os
import time


# selected place
#my_interest_place = "Casita - Museo del Ratón Pérez"
my_interest_place = ""
#my_interest_place = "Casita - Museo del Ratón Pérezzzzzzz"
file = "BiciMAD_nearest.csv"

def remove_results(f):
    if os.path.isfile(f):
        os.remove(f)

def save_results(df, f):
    df.to_csv(f)
            
def main():
    # remove results file, if exists
    remove_results(file)
    # load datasets
    places_dataset = api.load_datasets()
    # get place(s)
    df_my_place = api.get_place(my_interest_place, places_dataset)
    # if place(s) is found, get bicimad nearest
    if not df_my_place.empty:
        # get bicimad (from csv -> at home, from DB -> at ironhack)
        df_bicimad = bic.get_bicimad_data("CSV")
        #df_bicimad = get_bicimad_data("DB")
        if not df_bicimad.empty:
            ########## TODOOOOOOOOOO
            df_my_place = df_my_place[:10]
            ##########
            # get bicimad nearest for every place found
            df_bicimad_result = find.get_bicimad_nearest(df_my_place, df_bicimad)
            # save result as csv
            save_results(df_bicimad_result, file)
            print(f"save results in {file}")
        else:
            print(f"BiciMAD data not found")
    else:
        print(f"{my_interest_place} not found")


if __name__ == '__main__':
    start = time.time()
    print("start")
    main()
    end = time.time()
    print(f"time end: {end - start}")
