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
            return 0
        if len(data)<1:
            print("Not receiving full data... waiting for more")
            return
        # Make matrix of data
        line_arr = data.split(';')
        data_arr = [line.split(',') for line in line_arr]
        formatted_arr = [x[2:] for x in data_arr]

        # timestamp = data_arr[0]
        # counter = data_arr[1]
        # data_str = ",".join(data_arr[2:])
        # s = self.dh.receive(data_str)

        # Send it over for dealing
        s = self.dh.receive(formatted_arr)
        return s

    def reset(self):
        self.dh.reset()
