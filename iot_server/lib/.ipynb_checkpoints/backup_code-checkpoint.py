import os
import numpy as np
from numpy import *
import pandas as pd
import sensormotion as sm
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# -- Getting the data

"""
---------------------------------------------------------------------------------------------
count_steps code below
"""

'''
Function that gets the direcotries of dataframes
given main directory and list of indices of intereste datas
Example: get_data_raw('myfiles/data.cvs',[0,2])
'''


def get_data_raw(data_dir, data_index=[0]):
    data_all_dir = data_dir
    data_all_names = os.listdir(data_all_dir)
    data_names = [data_all_names[i] for i in data_index]
    data_dir_names = [(data_all_dir + name) for name in data_names]
    print('Datatsets used\n:{}'.format(data_dir_names))
    return data_dir_names


'''
Function that returns list of data-frames given list of directories
'''


def get_data_frame(files_dir_list):
    data_frame_list = []
    for file_name in files_dir_list:
        data_df = pd.read_csv(file_name, header=11)
        data_frame_list.append(data_df)
    return data_frame_list


# -- Filter Functions

'''
Function setting up the butterworth filter
returns the two parameters to pas sto filter_signal()
'''


def get_low_pass_filter(frequency=12, sample_rate=100, filter_type='low', filter_order=9):
    b, a = sm.signal.build_filter(frequency=frequency,
                                  sample_rate=sample_rate,
                                  filter_type=filter_type,
                                  filter_order=filter_order)
    return b, a


'''
Function returns a filtered signal
    b,a       - get them from get_low_pass_filter()
    my_signal - 1 dimensional signal data
'''


def filter_signal(b, a, my_signal):
    return sm.signal.filter_signal(b, a, signal=my_signal)


# -- Applying the filters

'''
Function that filters dataset and returns filtered data
input - numpy array; data is column separated
'''


def get_filtered_steps(my_data):
    lp_b, lp_a = get_low_pass_filter()
    my_data_filtered = np.array([filter_signal(lp_b, lp_a, my_signal) for my_signal in my_data.T])
    # print(my_data_filtered)
    peaks, x = find_peaks(my_data_filtered[0], height=(None, None))
    troughs, y = find_peaks(-my_data_filtered[0], height=(None, None))

    # print("Peaks: ")
    peaks_coord = pd.Series(x['peak_heights'].tolist())
    # print(peaks_coord)

    # print(type(my_data_filtered))
    # print(my_data_filtered[0].tolist())
    #     print("Troughs: ")

    troughs_coord = []
    for trough in troughs:
        troughs_coord.append(float(my_data_filtered[0].tolist()[trough]))  # pd.Series(y['peak_heights'].tolist())
    troughs_coord = pd.Series(troughs_coord)

    #     print('My data as list ', my_data.tolist())
    #     print('Trough indexes ', troughs)#troughs)
    #     print('Trough coords ', troughs_coord)

    # print('abs results ',(abs(peaks_coord-troughs_coord)))
    # print('max diff ', max((abs(peaks_coord-troughs_coord))))
    counter = 0
    for distance in abs(peaks_coord - troughs_coord):
        if distance > 0.05:
            counter += 1
    print(counter * 2)
    return counter * 2


def get_filtered_data(my_data):
    lp_b, lp_a = get_low_pass_filter()
    my_data_filtered = np.array([filter_signal(lp_b, lp_a, my_signal) for my_signal in my_data.T])
    # print(my_data_filtered)
    peaks, x = find_peaks(my_data_filtered[0], height=(None, None))
    troughs, y = find_peaks(-my_data_filtered[0], height=(None, None))

    # print("Peaks: ")
    peaks_coord = pd.Series(x['peak_heights'].tolist())
    # print(peaks_coord)

    # print(type(my_data_filtered))
    # print(my_data_filtered[0].tolist())
    #     print("Troughs: ")

    troughs_coord = []
    for trough in troughs:
        troughs_coord.append(float(my_data_filtered[0].tolist()[trough]))  # pd.Series(y['peak_heights'].tolist())
    troughs_coord = pd.Series(troughs_coord)

    #     print('My data as list ', my_data.tolist())
    #     print('Trough indexes ', troughs)#troughs)
    #     print('Trough coords ', troughs_coord)

    # print('abs results ',(abs(peaks_coord-troughs_coord)))
    # print('max diff ', max((abs(peaks_coord-troughs_coord))))
    counter = 0
    for distance in abs(peaks_coord - troughs_coord):
        if distance > 0.1:
            counter += 1
    # print(counter*2)
    return my_data_filtered


# -- Step calculation phase
'''
Function calculates the number of steps given data and desired axis
my_df     - the data-frame; should hold all data; n x m
my_dim    - the desired dimesion; [String]; ex: ['accel_x']
steps     - return of the function
steps     = len(minima) + len(maxima)
'''


def calcualate_steps(my_df, my_dim):
    my_signal = my_df[my_dim].values
    my_signal_filtered = get_filtered_data(my_data=my_signal)
    my_min, my_max = get_min_max(my_signal=my_signal.T[0])
    my_signal_filtered[0].shape
    my_min_fil, my_max_fil = get_min_max(my_signal=my_signal_filtered[0])
    #     print('my_min={}\nmy_max={}\nmy_min_filtered={}\nmy_max_filtered={}'
    #               .format(my_min,my_max,my_min_fil,my_max_fil))
    steps = len(my_max_fil) + len(my_min_fil)
    #     print("Size of max: " + str(len(my_max)) + " Size of min: "+ str(len(my_min)))
    #     print(my_max)
    #     print("\n")
    print(my_min_fil)
    return steps



"""
---------------------------------------------------------------------------------------------
Data Handler extra code below
"""


def recalculate(self):
    df = self.db.iloc[-1]
    th = max(self.db['accel_x']) - (max(self.db['accel_x']) - min(self.db['accel_x'])) * 0.23
    print('accel x and th', df['accel_x'], th)
    if df['accel_x'] > th:
        self.step_count += 1


def recalculate_windowed(self):
    df = self.db.iloc[-1]
    windowed_frame = self.db.tail(20)
    th = max(windowed_frame['accel_x']) - (max(windowed_frame['accel_x']) - min(windowed_frame['accel_x'])) * 0.23
    print('accel x and th', df['accel_x'], th)
    if df['accel_x'] > th:
        self.step_count += 1


def recalculate_peaks(self):
    df = self.db.iloc[-1]
    lst = []
    list_size = 0
    list_size = len(lst)

    # window stuff
    windowed_frame = self.db.tail(20)

    peaks, _ = find_peaks(self.db['accel_x'])
    for x in peaks:
        if self.db['accel_x'][x] > -0.52:
            lst.append(x)
    self.step_count = len(lst) * 2


def recalculate_threshold(self):
    df = self.db.iloc[-1]
    th = -0.79
    print('accel x and th', df['accel_x'], th)
    if df['accel_x'] > th:
        self.step_count += 1


def recalculate_filtered(self):
    df = self.db

    xacc_df = pd.DataFrame(df['accel_x'], columns=['accel_x'])
    yacc_df = pd.DataFrame(df['accel_y'], columns=['accel_y'])
    zacc_df = pd.DataFrame(df['accel_z'], columns=['accel_z'])

    average_xyz = (count_steps.run(xacc_df) + count_steps.run(yacc_df, ) + count_steps.run(zacc_df)) / 3
    self.step_count = average_xyz  # count_steps.run(yacc_df,plot=False)


def recalculate_filtered_magnitude(self):
    df = self.db

    xacc_df = pd.DataFrame(df['accel_x'], columns=['accel_x'])
    yacc_df = pd.DataFrame(df['accel_y'], columns=['accel_y'])
    zacc_df = pd.DataFrame(df['accel_z'], columns=['accel_z'])

    pd_merge = pd.concat([xacc_df, yacc_df, zacc_df], axis=1)
    pd_merge = pd_merge.values.tolist()

    d = {'mag_ax': []}
    mag_df = pd.DataFrame(data=d)
    i = 0
    for x, y, z in pd_merge:
        i += 1
        mag_df.loc[i] = math.sqrt(x * x + z * z + y * y)
    #     print(x,y,z)
    self.step_count = count_steps.run(mag_df)
