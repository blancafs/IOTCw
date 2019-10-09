import sys
import os
path = os.path.dirname(os.path.realpath(__file__))
path += '/../'
sys.path.append(path)
from libs.data_handler import DataHandler
from libs.configuration import TEST_STRINGS


dh = DataHandler()

for i in TEST_STRINGS:
    print(dh.receive(i))
