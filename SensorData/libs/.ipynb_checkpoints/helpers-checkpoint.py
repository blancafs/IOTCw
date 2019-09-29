# Helper methods stored here
from libs.configuration import DATA_COLUMN_NAMES
import pandas as pd


'''
Parse method takes a string of floats and returns a dataframe with a sole entry of those readings with the correct headings.
'''
def parse(data_string):
    data_arr = [float(i) for i in data_string.split(',')]
    df = pd.DataFrame(columns=DATA_COLUMN_NAMES)
    df.loc[0] = data_arr
    return df
