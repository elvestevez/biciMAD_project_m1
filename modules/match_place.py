from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd


def get_match(description, element, df):
    # get list elements
    list_titles = df[element].tolist()
    # match title
    matched_title = process.extractOne(description, list_titles, score_cutoff=80)
    # get df for match title
    if matched_title != None:
        df_selected = df[df[element] == matched_title[0]]
    else:
        df_selected = pd.DataFrame([])
    return df_selected
