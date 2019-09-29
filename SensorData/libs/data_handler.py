# Class to handle data coming in from Nordic Thingy in manner of a string=gyrox, gyroy, gyroz ... etc

# Imports
import pandas as pd
from libs.configuration import DATA_COLUMN_NAMES
from libs.helpers import parse

class DataHandler:

    def __init__(self):
        self.db = pd.DataFrame(columns=DATA_COLUMN_NAMES)
        self.step_count = 0

    def recalculate(self):
        if self.stopped:
            return "STOPPED"
        df = self.db.iloc[-1]
        th = max(self.db['accel_x']) - (max(self.db['accel_x'])-min(self.db['accel_x']))*0.17
        print('accel x and th', df['accel_x'], th)
        if df['accel_x']>th:
            self.step_count += 2

    '''
    The receive method handles data string, adds it to the database and returns the number of steps up to date.

    Uses method recalculate to update step count.
    '''
    def receive(self, data_string):
        entry = parse(data_string)
        self.db = self.db.append(entry, ignore_index=True)

        self.recalculate()
        return self.step_count

    def reset(self):
        self.db = pd.DataFrame(columns=DATA_COLUMN_NAMES)
        self.step_count = 0
