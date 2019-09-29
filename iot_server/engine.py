import sys
sys.path.append('/mnt/c/Users/Blanca/Desktop/IOTCw/SensorData/')
from libs.data_handler import DataHandler
from libs.configuration import TEST_STRINGS

class Engine:

    def __init__(self):
        self.dh = DataHandler()

    def dealWithData(self, data):
        s = self.dh.receive(data)
        return s
