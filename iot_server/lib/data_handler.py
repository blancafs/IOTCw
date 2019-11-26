# Class to handle data coming in from Nordic Thingy in manner of a string=gyrox, gyroy, gyroz ... etc
import os, sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

# Imports
import pandas as pd

from configuration import DATA_COLUMN_NAMES
from helpers import inRange, gfilter, applyRelu
from debug import Debug
from my_formatter import Formatter
from updaterBuilder import UpdaterBuilder

from scipy.signal import find_peaks
#import count_steps

class DataHandler(Debug):

    def __init__(self):
        self.db = pd.DataFrame(columns=DATA_COLUMN_NAMES)
        self.last_accy = -1
        self.first_peak = -1
        self.counter = 0
        self.lines_received = 0
        
        #ari variables
        self.windowed_frame = self.db.copy()
        #self.lst=[]

        # Get updater object
        self.updater = UpdaterBuilder.getUpdater()
        

        
    '''
    The receive method handles a 2D array containing arbitrary number of data lines (already separated as lists) adds it to the database and returns the number of steps up to date.

    Uses method recalculate to update step count.
    '''
    def receive(self, data):
        # Format the incoming data string
        self.log(data)
        data_matrix = Formatter.getDataMatrix(data)
        self.log('data matrix was formatted')

        # Update lines received
        self.lines_received += len(data_matrix)

        for entry in data_matrix:
            self.db = self.db.append(entry, ignore_index=True)

        # Change method below to change step detection algorithm
        if self.lines_received > 30:
            self.updater.update(self.db)
            #self.recalculate_filtered_magnitude()#input self.db
        
        return self.updater.getStepCount()

    def reset(self):
        self.db = pd.DataFrame(columns=DATA_COLUMN_NAMES)
        self.updater.reset()
