import serial
import time
import numpy as np
import scipy.signal

time_range = 8400 #how many times should the loop run? this is equal to the total time of the experiment (in s) divided by three
time_step = 30.0 #time between measurements ex. 3 seconds

tof = np.linspace(0,10,4000) #create a numpy array for all ToF values

high_amp_range = [319.1, 391.4] #specify amplitude range for high gain data
tof_range = [8.558, 9.798] #specify ToF range 
normal_amp_range = [254.1, 274.0] #specify amplitude range for normal gain data
#all these were determined by running experimental data for normal cell cycling
#the values are representative of the +/-3% of the typical range of amplitude and ToF values

proceed = True

def find_echo(file_name): #define a function
    """ 
    this function finds the amplitude and time of flight value of the 1st echo peak for a single file
    
    the function reads a single file and saves the data into a numpy array
    all peaks are found using scipy function and peaks appearing after 7.5 microseconds are selected
    the highest peak (with highest amplitude value) within that region is chosen to be the first echo peak
    corresponding time of flight value for the peak is found
    
    parameters:
        file_name is a path to the text file with amplitude data; the values are in a time series (in a csv format)
        
    returns:
        tof_value - the time of flight of the first echo peak
        amp_value - amplitude value of the first echo peak
     """

    data_list = [] #variable for storing data from a single file
    
    with open(file_name, 'r') as file: #read the file 
        text = file.read().replace('\n','')
        items = text.split(',')
        items_array = np.array(items) #put the data into a numpy array
        items_clean = np.delete(items_array,-1)
        numbers = items_clean.astype('int32') #convert the data from string to integer
        
        data_list.append(numbers)
        
    amp_array = np.vstack(data_list) #transform a list into numpy array
    
    peaks = scipy.signal.find_peaks((amp_array[0]), height = 200) #find all peaks

    peaks_high_tof = peaks[0]>3000 #find the peaks above 7.5 us
    
    amp_value = peaks[1]['peak_heights'][peaks_high_tof].max() #find the 1st echo peak amplitude value

    tof_index = np.where(peaks[1]['peak_heights'] == amp_value)[0][-1] 
                                        #find the index of ToF of 1st echo peak
    tof_value = tof[peaks[0][tof_index]] #find the corresponding ToF value
    
    return tof_value, amp_value #this spits out two values for every file

for count, x in enumerate(range(time_range)):
    
    starttime = time.time()
    
    ser = serial.Serial('COM3') #specify port
    ser.write(str.encode('param_RawData=0,10\r\n')) #send signal
    measurement = ser.readline() #save the recorded signal
    ser.close() #close to avoid errors
    
    amp_list = [] # create an empty list
    sep_bytes = measurement.split(b',') #separate the bytes
    for amp_data in sep_bytes: #iterate overthe bytes, convert to integers, save to a list
        amp_list.append(int(amp_data)) 
    
    f= open(f'C:\\Users\\Lab\\.spyder-py3\\FUSE_intern\\data_ex2\\Cell data ({count}).txt','w+')
    for count2, data in enumerate(amp_list):
        if count2 == len(amp_list)-1:
            info = str(data)
        else:
            info = str(data) +', '
        f.write(info)
    f.close()
    
    if proceed == True:
        tof_value, amp_value = find_echo(f'C:\\Users\\Lab\\.spyder-py3\\FUSE_intern\\data_ex2\\Cell data ({count}).txt')
    #save the values from the find_echo function
        #print("ToF is " + str(np.round(tof_value, 3)) + " us")
        #print("Amplitude is " + str(amp_value))
    
    
    if (tof_value < tof_range[0] or tof_value > tof_range[1]) and proceed == True:
        #decide if the values are appropriate
        stop_time = time_step * count
        
        result = ('Warning! '+ 'ToF is '+ str(np.round(tof_value, 3)) + '. Time is '+ str(stop_time) + ' s')
        #tell the user to stop the experiment
        proceed = False
        print(result)
    
    elif amp_value < normal_amp_range[0] and proceed == True: #decide if the values are appropriate
        stop_time = time_step * count
        result = ('Warning! '+ 'Amplitude is too low' + '. Time is '+ str(stop_time) + ' s')
        #tell the user to stop the experiment
        proceed = False
        print(result)
        
    if count == time_range-1:
        print("Experiment completed")
        
    #print()
    time.sleep(time_step - ((time.time() - starttime) % time_step))



