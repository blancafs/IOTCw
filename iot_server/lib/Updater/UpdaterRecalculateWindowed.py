import os, sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)
sys.path.append(path+'../')

from helpers import *

from updater import Updater

class UpdaterRecalculateWindowed(Updater):
    def update(self, db):
        df = db.iloc[-1]
        th = max(db['accel_x']) - (max(db['accel_x']) - min(db['accel_x'])) * 0.23
        print('accel x and th', df['accel_x'], th)
        if df['accel_x'] > th:
            self.step_count += 1