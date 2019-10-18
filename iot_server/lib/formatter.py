import os, sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

import pandas as pd
from configuration import DATA_COLUMN_NAMES

'''
Class deals with formatting the data string
Returns a data matrix:
    2D matrix containing lists of data lines
'''
class Formatter:

    @staticmethod
    def parse(data_arr):
        data_arr = [float(i) for i in data_arr]
        df = pd.DataFrame(columns=DATA_COLUMN_NAMES)
        df.loc[0] = data_arr
        return df


    """
    Gets a string and splits necessary information
    Input "a,b,c;a,b,c"
    Output [[a,b,c][a,b,c]]
    """

    @staticmethod
    def getDataMatrix(data):
        lines = data.split(';')
        data_matrix = [line.split(',') for line in lines]

        # Data unique formatting
        # Remove the first two elements (timestamp,sequence)
        formatted_matrix = [x[2:] for x in data_matrix]
        formatted_matrix = [Formatter.parse(x) for x in formatted_matrix]
        return formatted_matrix