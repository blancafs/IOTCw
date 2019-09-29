import sys
sys.path.append('/mnt/c/Users/Blanca/Desktop/IOTCw/SensorData/')
from libs.data_handler import DataHandler
from libs.configuration import TEST_STRINGS


dh = DataHandler()

for i in TEST_STRINGS:
    print(dh.receive(i))
