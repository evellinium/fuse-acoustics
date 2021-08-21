import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

data_folder = []

for num in range (7800):
    data_folder.append(f'C:\\Users\\Lab\\.spyder-py3\\FUSE_intern\\data_ex1\\Cell data ({num}).txt')

tof = np.linspace(0,10,4000)

data_list = []

for txt_file in tqdm(data_folder):
    with open(txt_file, 'r') as file:
        text = file.read().replace('\n','')
        items = text.split(',')
        items_array = np.array(items)
        numbers = items_array.astype('int32')
        data_list.append(numbers)
        
amp_array = np.vstack(data_list)


tof_axis = tof #np.array

stop_time = 3 * 7800 #time_step * (number of data points-1)
time = np.linspace(0,stop_time, num=7800)
time_axis = time

amp_axis = np.transpose(amp_array) #np.array

viridis = cm.get_cmap('viridis', 256)
newcolors = viridis(np.linspace(0, 1, 256))
newcmp = ListedColormap(newcolors)

def plot_examples(cms):
    """
    helper function to plot two colormaps
    """
    data = amp_axis
    #np.vstack((tof_axis, time_axis))

    fig, axs = plt.subplots(1, 2, figsize=(40, 10))
    for [ax, cmap] in zip(axs, cms):
        psm = ax.pcolormesh(time_axis, tof_axis, data, cmap=cmap, rasterized=True, vmin = 250)
        fig.colorbar(psm, ax=ax, label = 'Amplitude')
        
        ax.set_ylabel('ToF [\u03bcs]')
        ax.set_xlabel('Time [s]')
        plt.savefig(f'C:\\Users\\Lab\\.spyder-py3\\FUSE_intern\\high_c_rate_map.png')
        
    ax.hlines(8.558, 0, 252000, colors = 'white')
    ax.hlines(9.798, 0, 252000, colors = 'white')
    
    
    plt.show()
    
plot_examples([viridis, newcmp])