# Class to handle data coming in from Nordic Thingy in manner of a string=gyrox, gyroy, gyroz ... etc

# Imports
import math
import pandas as pd
from libs.configuration import DATA_COLUMN_NAMES
from libs.helpers import parse, inRange, gfilter, applyRelu
from scipy.signal import find_peaks
from . import count_steps

class DataHandler:

    def __init__(self):
        self.db = pd.DataFrame(columns=DATA_COLUMN_NAMES)
        self.step_count = 0
        self.last_accy = -1
        self.first_peak = -1
        self.counter = 0
        self.lines_received = 0
        
        #ari variables
        self.windowed_frame = self.db.copy()
        #self.lst=[]
        
    def recalculate(self):
        df = self.db.iloc[-1]
        th = max(self.db['accel_x']) - (max(self.db['accel_x'])-min(self.db['accel_x']))*0.23
        print('accel x and th', df['accel_x'], th)
        if df['accel_x']>th:
            self.step_count += 1
            
    def recalculate_windowed(self):
        df = self.db.iloc[-1]
        windowed_frame = self.db.tail(20)
        th = max(windowed_frame['accel_x']) - (max(windowed_frame['accel_x'])-min(windowed_frame['accel_x']))*0.23
        print('accel x and th', df['accel_x'], th)
        if df['accel_x']>th:
            self.step_count += 1

    def recalculate_peaks(self):
        df = self.db.iloc[-1]
        lst = []
        list_size = 0
        list_size = len(lst)
        
        #window stuff
        windowed_frame = self.db.tail(20)
        
        peaks, _ = find_peaks(self.db['accel_x'])
        for x in peaks:
            if self.db['accel_x'][x]>-0.52:
                lst.append(x)
        self.step_count=len(lst)*2

#         print(len(lst)*2)
#         self.step_count = len(self.lst)*2
#         windowed_frame = self.db.tail(20)
#         th = max(windowed_frame['accel_x']) - (max(windowed_frame['accel_x'])-min(windowed_frame['accel_x']))*0.23
#         print('accel x and th', df['accel_x'], th)
#         if df['accel_x']>th:
#             self.step_count += 1
    
    def recalculate_threshold(self):
        df = self.db.iloc[-1]
        th = -0.69
        print('accel x and th', df['accel_x'], th)
        if df['accel_x']>th:
            self.step_count += 1
    
    def recalculate_filtered(self):
        df = self.db
        
        xacc_df = pd.DataFrame(df['accel_x'], columns=['accel_x'])
        yacc_df = pd.DataFrame(df['accel_y'], columns=['accel_y'])
        zacc_df = pd.DataFrame(df['accel_z'], columns=['accel_z'])
        
        average_xyz=(count_steps.run(xacc_df)+count_steps.run(yacc_df,)+count_steps.run(zacc_df))/3
        self.step_count = average_xyz #count_steps.run(yacc_df,plot=False)

    def recalculate_filtered_magnitude(self):
        df = self.db
        
        xacc_df = pd.DataFrame(df['accel_x'], columns=['accel_x'])
        yacc_df = pd.DataFrame(df['accel_y'], columns=['accel_y'])
        zacc_df = pd.DataFrame(df['accel_z'], columns=['accel_z'])
        
        pd_merge = pd.concat([xacc_df,yacc_df,zacc_df],axis=1)
        pd_merge = pd_merge.values.tolist()

        d = {'mag_ax': []}
        mag_df = pd.DataFrame(data=d)
        i =0
        for x,y,z in pd_merge:
            i += 1
            mag_df.loc[i]=math.sqrt(x*x + z*z + y*y)
        #     print(x,y,z)
        self.step_count = count_steps.run(mag_df)
        
        
    '''
    The receive method handles data string, adds it to the database and returns the number of steps up to date.

    Uses method recalculate to update step count.
    '''
    def receive(self, data_matrix):
        # Update lines received
        self.lines_received += len(data_matrix)

        # entry = parse(data_string)
        # self.db = self.db.append(entry, ignore_index=True)

        entries = [parse(line) for line in data_matrix]
        for entry in entries:
            self.db = self.db.append(entry, ignore_index=True)

        # Change method below to change step detection algorithm
        if self.lines_received >30:
            self.recalculate_filtered_magnitude()
#         df = self.db
#         xacc_df = pd.DataFrame(df['accel_x'], columns=['accel_x'])
#         print(xacc_df)
        
        return self.step_count

    def reset(self):
        self.db = pd.DataFrame(columns=DATA_COLUMN_NAMES)
        self.step_count = 0

# ATTEMPTED METHOD DO NOT DELETE

    # def recalculate(self):
    #     df = self.db.iloc[-1]
    #     th = max(self.db['accel_x']) - (max(self.db['accel_x'])-min(self.db['accel_x']))*0.23
    #     print('accel x and th', df['accel_x'], th)
    #     if df['accel_x']>th:
    #         self.step_count += 1
    #
    # def every2recalculate(self):
    #     print('last accy ', self.last_accy)
    #     print('first peak ', self.first_peak)
    #     print('counter ', self.counter)
    #     print('step count ', self.step_count)
    #     self.db = gfilter(self.db)
    #     self.db = applyRelu(self.db)
    #     df = self.db.iloc[-1]
    #     curr_accy = df['accel_y']
    #     if curr_accy<self.last_accy and self.first_peak==(-1):
    #         self.first_peak = 0.9*self.last_accy
    #         self.counter += 1
    #     self.last_accy = curr_accy
    #     if inRange(curr_accy, float(self.first_peak)*0.8, float(self.first_peak)*1.2) :
    #         self.counter +=1
    #     if self.counter==2:
    #         self.step_count +=2
    #         self.counter = 0
