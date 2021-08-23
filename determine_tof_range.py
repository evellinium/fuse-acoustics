import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import scipy.signal

no_of_files = 7800 #specify the number of files with amplitude data

data_folder = [] #create an empty list to store file paths 

for num in range (no_of_files): #iterate over the number of files
    data_folder.append(f'C:\\Users\\Lab\\.spyder-py3\\FUSE_intern\\data_ex1\\Cell data ({num}).txt') #append file paths corresponding to existing amplitude data files

tof = np.linspace(0,10,4000) #create an evenly spaced array of 4000 numbers between 0 and 10 microseconds

data_list = [] #create an empty list to store the data itself

for txt_file in tqdm(data_folder): #iterate over the file names in data_folder
    
    with open(txt_file, 'r') as file: #open the file
        text = file.read().replace('\n','') #read the file
        items = text.split(',') 
        items_array = np.array(items) #turn them into a numpy array
        numbers = items_array.astype('int32') #convert to integers
        data_list.append(numbers) #append the numbers to a list
        
amp_array = np.vstack(data_list) #turn the list into an array

amp_range = [1000,1] #create variables for range of the data, the first number will be the lower bound and the second will be an upper bound
tof_range = [1000, 1]
#1000 and 1 were used here because 1000 will be immediately replaced (as all values are lower than 1000) and 1 will also be released immediately (as all values are higher than 1)

for data in amp_array: #iterate over the signals in the amplitude array
    
    peaks = scipy.signal.find_peaks(data, height = 200) #find all peaks
    peaks_high_tof = peaks[0]>3000 #find the peaks positioned later than 7.5 microseconds (that is where the first echo peaks is found)

    amp_value = peaks[1]['peak_heights'][peaks_high_tof].max() #find the echo peak
    
    if amp_value < amp_range[0]: #compare the amplitude value of the 1st echo peak and exchange them if they are lower than the lower bound or higher than the upper bound
        amp_range[0] = amp_value
    if amp_value > amp_range[1]:
        amp_range[1] = amp_value

    tof_index = np.where(peaks[1]['peak_heights'] == amp_value)[0][-1] #find the index corresponding to time of flight
    tof_value = tof[peaks[0][tof_index]] #find the time of flight value of the first echo peak
    
    if tof_value < tof_range[0]: #compare the tof value of the 1st echo peak and exchange them if they are lower than the lower bound or higher than the upper bound
        tof_range[0] = tof_value
    if tof_value > tof_range[1]:
        tof_range[1] = tof_value
  

table_data = {'Dataset':  ['Normal'],   #save all the information to a table
              'Amplitude range': [amp_range],     
              'Amp +/- 3%' : [[round(amp_range[0]*0.97,1), round(amp_range[1]*1.03,1)]], #take +/- 3% from the lower and upper bounds to account for experimental uncertainties
             'Time of Flight range':[tof_range],
             'ToF +/- 3%' : [[round(tof_range[0]*0.97,3), round(tof_range[1]*1.03,3)]]}

df = pd.DataFrame (table_data, columns = ['Dataset','Amplitude range','Amp +/- 3%','Time of Flight range','ToF +/- 3%']) #put the data into a pandas data frame
print(df) 
