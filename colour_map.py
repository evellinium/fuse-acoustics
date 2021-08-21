import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

data_folder = [] #create an empty list to store data files

for num in range (7800): #iterate over the number of data files 
    data_folder.append(f'C:\\Users\\Lab\\.spyder-py3\\FUSE_intern\\data\\Cell data ({num}).txt') #create a list of file names matching the already existing files (this ensures the numbers are in order)

tof = np.linspace(0,10,4000) #create an evenly spaced array of 4000 numbers between 0 and 10 (microseconds), this is to indicate the time-of-flight values in the experiment

data_list = [] #create an empty list to store amplitude data

for txt_file in tqdm(data_folder): #iterate over the files in the data folder
    with open(txt_file, 'r') as file: #open the file to read (all files are in csv format)
        text = file.read().replace('\n','')
        items = text.split(',')
        items_array = np.array(items) #create a numpy array
        numbers = items_array.astype('int32') #turn the values to integers
        data_list.append(numbers) #append the values to a list
        
amp_array = np.vstack(data_list) #turn the amplitude data into a numpy array

tof_axis = tof #specify the data for y-axis

stop_time = 3 * 7800 #time_step * (number of data files-1)
time = np.linspace(0,stop_time, num=7800) #create an array of evenly spaced numbers representing the time of the experiment
time_axis = time #identify this as the x_axis

amp_axis = np.transpose(amp_array) # identify the third axis to be a transposed array of amplitude data

viridis = cm.get_cmap('viridis', 256) #define the colour for the colour map
newcolors = viridis(np.linspace(0, 1, 256)) 
newcmp = ListedColormap(newcolors)

def plot_examples(cms):
    """
    function to plot two colormaps
    """
    data = amp_axis

    fig, axs = plt.subplots(1, 2, figsize=(40, 10)) #create two plots
    for [ax, cmap] in zip(axs, cms):
        psm = ax.pcolormesh(time_axis, tof_axis, data, cmap=cmap, rasterized=True, vmin = 250) #specify axis and minimum amplitude value to show on the graph
        fig.colorbar(psm, ax=ax, label = 'Amplitude') #define the legend of the amplitude data
        
        ax.set_ylabel('ToF [\u03bcs]') #set label for y axis
        ax.set_xlabel('Time [s]') #set label for x axis
        plt.savefig(f'C:\\Users\\Lab\\.spyder-py3\\FUSE_intern\\high_c_rate_map.png') #save this as a png
        
    ax.hlines(8.558, 0, 252000, colors = 'white') #create two white lines for the safe operating range for ToF
    ax.hlines(9.798, 0, 252000, colors = 'white') 
    
    plt.show() 
    
plot_examples([viridis, newcmp]) #plot the colour map
