import os
import numpy as np
from numpy import *
import pandas as pd
import sensormotion as sm
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
# -- Getting the data

'''
Function that gets the direcotries of dataframes
given main directory and list of indices of intereste datas
Example: get_data_raw('myfiles/data.cvs',[0,2])
'''
def get_data_raw(data_dir, data_index=[0]):
    data_all_dir = data_dir
    data_all_names = os.listdir(data_all_dir)
    data_names = [data_all_names[i] for i in data_index]
    data_dir_names = [(data_all_dir+name) for name in data_names]
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
def get_low_pass_filter(frequency=12,sample_rate=100,filter_type='low',filter_order=9):
    b, a = sm.signal.build_filter(frequency=frequency,
                                  sample_rate=sample_rate,
                                  filter_type=filter_type,
                                  filter_order=filter_order)
    return b,a

'''
Function returns a filtered signal
    b,a       - get them from get_low_pass_filter()
    my_signal - 1 dimensional signal data
'''
def filter_signal(b,a,my_signal):
    return sm.signal.filter_signal(b, a, signal=my_signal)


# -- Applying the filters

'''
Function that filters dataset and returns filtered data
input - numpy array; data is column separated
'''


def get_filtered_steps(my_data):
    lp_b, lp_a = get_low_pass_filter()
    my_data_filtered = np.array([filter_signal(lp_b,lp_a,my_signal) for my_signal in my_data.T])
    #print(my_data_filtered)
    peaks, x = find_peaks(my_data_filtered[0], height=(None,None))
    troughs, y = find_peaks(-my_data_filtered[0], height=(None,None))
    
    #print("Peaks: ")
    peaks_coord = pd.Series(x['peak_heights'].tolist())
    #print(peaks_coord)
    
    #print(type(my_data_filtered))
    #print(my_data_filtered[0].tolist())
#     print("Troughs: ")
    
    troughs_coord = []
    for trough in troughs:
        troughs_coord.append(float(my_data_filtered[0].tolist()[trough])) #pd.Series(y['peak_heights'].tolist())
    troughs_coord = pd.Series(troughs_coord)
    
#     print('My data as list ', my_data.tolist())
#     print('Trough indexes ', troughs)#troughs)
#     print('Trough coords ', troughs_coord)
    
    #print('abs results ',(abs(peaks_coord-troughs_coord)))
    #print('max diff ', max((abs(peaks_coord-troughs_coord))))
    counter = 0
    for distance in abs(peaks_coord-troughs_coord):
        if distance > 0.05:
            counter +=1
    print(counter*2)
    return counter*2



def get_filtered_data(my_data):
    lp_b, lp_a = get_low_pass_filter()
    my_data_filtered = np.array([filter_signal(lp_b,lp_a,my_signal) for my_signal in my_data.T])
    #print(my_data_filtered)
    peaks, x = find_peaks(my_data_filtered[0], height=(None,None))
    troughs, y = find_peaks(-my_data_filtered[0], height=(None,None))
    
    #print("Peaks: ")
    peaks_coord = pd.Series(x['peak_heights'].tolist())
    #print(peaks_coord)
    
    #print(type(my_data_filtered))
    #print(my_data_filtered[0].tolist())
#     print("Troughs: ")
    
    troughs_coord = []
    for trough in troughs:
        troughs_coord.append(float(my_data_filtered[0].tolist()[trough])) #pd.Series(y['peak_heights'].tolist())
    troughs_coord = pd.Series(troughs_coord)
    
#     print('My data as list ', my_data.tolist())
#     print('Trough indexes ', troughs)#troughs)
#     print('Trough coords ', troughs_coord)
    
    #print('abs results ',(abs(peaks_coord-troughs_coord)))
    #print('max diff ', max((abs(peaks_coord-troughs_coord))))
    counter = 0
    for distance in abs(peaks_coord-troughs_coord):
        if distance > 0.1:
            counter +=1
    #print(counter*2)
    return my_data_filtered


# -- Minima and Maxima calulations

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
    my_min,my_max = get_min_max(my_signal=my_signal.T[0])
    my_signal_filtered[0].shape
    my_min_fil,my_max_fil = get_min_max(my_signal=my_signal_filtered[0])
#     print('my_min={}\nmy_max={}\nmy_min_filtered={}\nmy_max_filtered={}'
#               .format(my_min,my_max,my_min_fil,my_max_fil))
    steps = len(my_max_fil)+len(my_min_fil)
#     print("Size of max: " + str(len(my_max)) + " Size of min: "+ str(len(my_min)))
#     print(my_max)
#     print("\n")
    print(my_min_fil)
    return steps

# -- Fast function to do all of it given one dataset

'''
Function used to quickly do everything given data directory and index
'''
def run(data_frame,plot=False):
    #data_names_list = get_data_raw(data_dir,data_index=[idx])
    #data_frame_list = get_data_frame(data_names_list)
    #print(data_frame)
    df = data_frame.copy()
    #print(df.columns)
    dim = [df.columns[0]]#['accel_z']#df.columns[0]#['accel_y']#['accel_x'] #data_frame[data_frame.columns[0]]
    #print(df)
    steps = get_filtered_steps(df[dim].values)
    #steps = calcualate_steps(my_df=df,my_dim=dim)
    #print('Approximate number of steps: {}'. format(steps))
    print("Steps for "+str(df.columns[0])+ ": "+str(steps))
    if(plot==True):
        plot_filter_vs_unfiltered(data_frame,
                              dimensions_list=dim,
                              data_points=200,
                              color='red',min_max=True)
    return steps
