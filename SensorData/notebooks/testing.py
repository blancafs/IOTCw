import sys
import os
path = os.path.dirname(os.path.realpath(__file__))
path += '/../'
sys.path.append(path)

from libs.data_handler import DataHandler
from libs.configuration import TEST_STRINGS


dh = DataHandler()

for i in TEST_STRINGS:
    # Separate the string in comas and turn it in a data list
    list_i = i.split(',')
    
    # Add list to data matrix as the receive accepts a double matrix
    data_matrix = [list_i]
    print(dh.receive(data_matrix))
