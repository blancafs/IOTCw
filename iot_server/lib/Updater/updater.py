import os, sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

from debug import Debug
from helpers import *

"""
Abstract class that implements the recalculation of the steps
"""
class Updater(Debug):

    def __init__(self):
        self.step_count = 0

    def reset(self):
        self.step_count = 0

    def getStepCount(self):
        return self.step_count


    # IMPLEMENT THESE METHODS
    def update(self, db):
        pass

    def count_steps(self, db):
        pass


"""
IMPLEMENTATIONS ------------------------------------------------------------------------------------

class Updater_NAME(Updater):
    # Important! updates step count
    def update(self):
        pass
        
    # IF using count_steps.run then the code below implements the count steps method
    def count_steps(self, my_data):
        pass
        
"""

# UPDATER FILTERED MAGNITUDE SUBCLASS
