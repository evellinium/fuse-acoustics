This is a Faraday Undegraduate Summer Experience project about acoustic analysis of Li-ion batteries.

Description of the files in this repository

experiment_run.py 
This code was used to run the experiment during the project. It includes communication with an ultrasonic flaw detector EPOCH 650 for acoustic analysis of a lithium-ion battery and tracking the 'first echo peak' as a way to monitor battery failure. The code produces a warning if the first echo peak moves beyond a certain range or starts to vanish in order to warn the user about incoming battery failure.

colour_map.py
Creates a colour map from a folder with csv files containing amplitude data collected by EPOCH 650 (as shown in experiment_run.py). The colour map is a great way to visualise acoustic data collected throughout the experiment and can provide insight into changes in the internal structure of the battery.

determine_range.py
This code goes through the acoustic data of a battery during standard operation to establish the standard range of time-of-flight and amplitude of the first echo peak. The results from this were later used in experiment_run.py to know when the battery is no longer in the safe operating window.
