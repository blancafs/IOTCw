# Helper methods stored here
from libs.configuration import DATA_COLUMN_NAMES
import pandas as pd
from scipy.ndimage import gaussian_filter

'''
Parse method takes a string of floats and returns a dataframe with a sole entry of those readings with the correct headings.
'''
def parse(data_arr):
    data_arr = [float(i) for i in data_arr]
    df = pd.DataFrame(columns=DATA_COLUMN_NAMES)
    df.loc[0] = data_arr
    return df

def inRange(num, float1, float2):
    if num >= float1 and num<=float2:
        return True
    return False

def gfilter(df, cols_to_filter=DATA_COLUMN_NAMES):
    for c in cols_to_filter:
        df[c] = gaussian_filter(df[c].values, sigma=1)
    return df

def applyRelu(df):
    for i in df.columns:
        df.loc[df[i]<0, i] = 0
    return df
