import sys
import os
path = os.path.dirname(os.path.realpath(__file__))
path += '/../SensorData'

print(path)
sys.path.append(path)
from libs.data_handler import DataHandler
from libs.configuration import TEST_STRINGS

class Engine:

    def __init__(self):
        self.dh = DataHandler()

    def dealWithData(self, data):
        if data=="RESET":
            self.reset()
        data_arr = data.split(',')
        timestamp = data_arr[0]
        counter = data_arr[1]
        data_str = ",".join(data_arr[2:])
        s = self.dh.receive(data_str)
        return s

    def reset(self):
        self.dh.reset()
