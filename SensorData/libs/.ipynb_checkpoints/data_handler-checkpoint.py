# Class to handle data coming in from Nordic Thingy in manner of a string=gyrox, gyroy, gyroz ... etc

# Imports
import pandas as pd
from libs.configuration import DATA_COLUMN_NAMES
from libs.helpers import parse

class DataHandler:

    def __init__(self):
        self.db = pd.DataFrame(columns=DATA_COLUMN_NAMES)
        
    def recalculate(self):
        pass

    # Handle data string add to db and return number of steps up to date
    def receive(self, data_string):
        
        # Making sure data received fits format expected
        entry = parse(data_string)
        
        if len(entry)==6:
            self.db[self.db.index] = entry
        else:
            print('Data given did not match the length expected')
        
        # Having added latest entry return the current count of steps
        steps = self.recalculate()
        steps = 5
        return steps

    def reset(self):
        self.db = pd.DataFrame(columns=DATA_COLUMN_NAMES)

    
        
        