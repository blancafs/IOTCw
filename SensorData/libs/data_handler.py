# Class to handle data coming in from Nordic Thingy in manner of a string=gyrox, gyroy, gyroz ... etc

# Imports
import pandas as pd
from libs.configuration import DATA_COLUMN_NAMES
from libs.helpers import parse, inRange, gfilter, applyRelu

class DataHandler:

    def __init__(self):
        self.db = pd.DataFrame(columns=DATA_COLUMN_NAMES)
        self.step_count = 0
        self.last_accy = -1
        self.first_peak = -1
        self.counter = 0

    def inRange(num, float1, float2):
        if num >= float1 and num<=float2:
            return True
        return False

    def recalculate(self):
        df = self.db.iloc[-1]
        th = max(self.db['accel_x']) - (max(self.db['accel_x'])-min(self.db['accel_x']))*0.17
        print('accel x and th', df['accel_x'], th)
        if df['accel_x']>th:
            self.step_count += 2

    def every2recalculate(self):
        print('last accy ', self.last_accy)
        print('first peak ', self.first_peak)
        print('counter ', self.counter)
        print('step count ', self.step_count)
        self.db = gfilter(self.db)
        self.db = applyRelu(self.db)
        df = self.db.iloc[-1]
        curr_accy = df['accel_y']
        if curr_accy<self.last_accy and self.first_peak==(-1):
            self.first_peak = 0.9*self.last_accy
            self.counter += 1
        self.last_accy = curr_accy
        if inRange(curr_accy, float(self.first_peak)*0.8, float(self.first_peak)*1.2) :
            self.counter +=1
        if self.counter==2:
            self.step_count +=2
            self.counter = 0

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
