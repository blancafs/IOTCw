import sys
import os
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

from data_handler import DataHandler
from debug import Debug

class Engine(Debug):

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
        # line_arr = data.split(';')
        # data_arr = [line.split(',') for line in line_arr]
        # formatted_arr = [x[2:] for x in data_arr]

        # Send it over for dealing
        s = self.dh.receive(data)
        return s

    def reset(self):
        self.dh.reset()
