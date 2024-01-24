#-------------------------------IMPORT------------------------------------------
import machine
import time
from machine import I2C
import math
import pycom
from SI7006A20 import SI7006A20 # Import the class in order to make object later
#-------------------------------------GET VALUES--------------------------------
'''This function takes in noting as an argument, creates an SI7006A20 object
     which we can use to get sensor data on external temprature in celcius.
     Returns temprature data (float)'''

def get_data():
    si = SI7006A20()
    temp = si.temperature()
    # We print the data here so we can check that it correponds
    # to what is presented on Datacakes
    print(int(temp)) # Easier on the eye to get an integer presented!
    return temp



pycom.heartbeat(False)

# Phase 1 is heating
Heating = True
while Heating: # Whilst we heat up the hot tool, get temprature and publish it
    pycom.rgbled(0xFF0000)  # Blink red during this phase
    temp = get_data()
    print(str(int(temp)))
    time.sleep(10)

    # Note: This threshold might be different for different people, play around with it!
    # Check if our temp is above 70 celisus, if yes then our hot tool is hot enough and we exit loop
    # Else we get new temprature (While loop continues)
    if temp > 70: # Change if needed
        print('I am hot enough now!')
        Heating = False
        Cooldown = True # Triggers next phase

# Phase 2 is cooling down
i = 0 # Our cooldown time will be calculated using a simple counter
while Cooldown:
    pycom.rgbled(0x0000FF) # Blink Blue during this phase
    temp = get_data()
    print(str(int(temp)))
    time.sleep(10)
    i += 10 # Add 10 sec to counter (Since we waited 10 since last time)

    # Note: This threshold might be different for different people, play around with it!
    if temp < 36: # Change if needed
        print('cooldown time done: ', i, 'Secs')
        Cooldown = False
#------------------------------------------------------------------------------
