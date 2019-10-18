import os, sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

# HERE SET WHICH FILE YOU WANT TO USE
from Updater.UpdaterFilteredMagnitude import UpdaterFilteredMagnitude
UPDATER_CLASS = UpdaterFilteredMagnitude

class UpdaterBuilder:

    @staticmethod
    def getUpdater():
        updater = UPDATER_CLASS()
        return updater