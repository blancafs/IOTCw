# Helper methods stored here
import os, sys
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path)

import math
from configuration import DATA_COLUMN_NAMES
import pandas as pd
from scipy.ndimage import gaussian_filter
import sensormotion as sm
import numpy as np
from scipy.signal import find_peaks

'''
Parse method takes a string of floats and returns a dataframe with a sole entry of those readings with the correct headings.
'''

def inRange(num, float1, float2):
    if num >= float1 and num<=float2:
        return True
    return False

def gfilter(df, cols_to_filter=DATA_COLUMN_NAMES):
    for c in cols_to_filter:
        df[c] = gaussian_filter(df[c].values, sigma=1)
    return df

def applyRelu(df):
    for i in df.columns:
        df.loc[df[i]<0, i] = 0
    return df


'''
Function that returns minima and maxima values given 1 dimensional sinal
'''
def get_min_max(my_signal):
    data = my_signal
    x = np.linspace(0,data.shape[0],data.shape[0])
    # Calculating the points:
    my_min_max = diff(sign(diff(data))).nonzero()[0] + 1 # local min+max
    my_min = (diff(sign(diff(data))) > 0).nonzero()[0] + 1 # local min
    my_max = (diff(sign(diff(data))) < 0).nonzero()[0] + 1 # local max
    # return the results
    return [my_min,my_max]

# -- Plotting

'''
Function that plots the minima and maxima of of a 1 dimesional signal
'''
def plot_min_max(my_signal,axis):
    data = my_signal
    x = linspace(0,data.shape[0],data.shape[0])
    # Calculating the points:
    a = diff(sign(diff(data))).nonzero()[0] + 1 # local min+max
    b = (diff(sign(diff(data))) > 0).nonzero()[0] + 1 # local min
    c = (diff(sign(diff(data))) < 0).nonzero()[0] + 1 # local max
    # Plotting the minima & maxima
    axis.plot(x,data)
    axis.plot(x[b], data[b], "o", label="min")
    axis.plot(x[c], data[c], "o", label="max")


'''
Function comapre filtered vs unfiltered data & plots it
    my_df           - dataframe of all data
    dimensions_list - headers to select for comparrison
    datapoints      - how many points to display
    color           - color of text around the plot
    min_max         - in case you want to find the min and max and plot them
'''
def plot_filter_vs_unfiltered(my_df,dimensions_list=['accel_x'],
                              data_points=200,color='black',
                              min_max=True):
    my_title = 'Data:\n'+', '.join(dimensions_list)
    my_legend = [dim+'_filtered' for dim in dimensions_list]
    my_legend_full = dimensions_list+my_legend
    # get in numpy format
    my_df_selected = my_df[dimensions_list].values
    # filter the data
    my_df_selected_filtered = get_filtered_data(my_df_selected)
    # Plotting & calculating Minima & Maxima if needed
    fig,axis=plt.subplots(1,1,figsize=(20,10))
    if(min_max==False):
        #axis.plot(my_df_selected[0:data_points])
        axis.plot(my_df_selected_filtered[0:data_points].T)
        plt.legend(my_legend_full,fontsize='xx-large')
    elif(min_max==True):
#         for my_signal in my_df_selected.T:
#             plot_min_max(my_signal,axis)
        for my_signal in my_df_selected_filtered:
            plot_min_max(my_signal,axis)
    axis.set_title(my_title,fontsize=30,color=color)
    axis.tick_params(axis='both', colors=color,labelsize=20)
    axis.grid()
    plt.show()

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