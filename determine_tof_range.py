import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import scipy.signal


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

amp_range = [1000,1]
ex_tof_range = [9.1, 9.2]

for data in amp_array:
    peaks = scipy.signal.find_peaks(data, height = 200)
    #print(peaks)
    peaks_high_tof = peaks[0]>3000 #find the peaks in the range 7.5 to 10 us

    amp_value = peaks[1]['peak_heights'][peaks_high_tof].max() #find the echo peak
    #print(amp_value)
    
    if amp_value < amp_range[0]:
        amp_range[0] = amp_value
    if amp_value > amp_range[1]:
        amp_range[1] = amp_value

    tof_index = np.where(peaks[1]['peak_heights'] == amp_value)[0][-1]
    tof_value = tof[peaks[0][tof_index]] #find the corresponding ToF value
    
    if tof_value < ex_tof_range[0]:
        ex_tof_range[0] = tof_value
    if tof_value > ex_tof_range[1]:
        ex_tof_range[1] = tof_value
    
    #amp_range.append(amp_value)
    #tof_range.append(tof_value)
    #maybe append the values to a list? or create bounds and alter them as you go?
    
    
    #add 3%
    
    #then maybe think about a poster
print(ex_tof_range)
print(amp_range)

x_axis = tof #x and y axis for the signal graph
y_axis = amp_array[0]
plt.plot(x_axis, y_axis)
plt.show()

old_tof_range_3 = [8.558, 9.798]
old_tof_range = [8.822, 9.512]


table_data = {'Dataset':  ['Recent experiment', 'Reference'],
             'Time of Flight range':[[round(ex_tof_range[0],3),round(ex_tof_range[1],3)], old_tof_range],
             'ToF +/- 3%' : [['NaN', 'NaN'], old_tof_range_3]}

df = pd.DataFrame (table_data, columns = ['Dataset', 'Time of Flight range','ToF +/- 3%'])
print(df)