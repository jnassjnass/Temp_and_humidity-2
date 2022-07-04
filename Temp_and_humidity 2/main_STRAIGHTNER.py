#-------------------------------IMPORT------------------------------------------
import time
from machine import I2C
import math
import machine
import pycom
from SI7006A20 import SI7006A20 # Import the class in order to make object later
from mqtt import MQTTClient # Import the class in order to make object later
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
#----------------------------CONNECT TO DATACAKES-------------------------------
# Note: This code is derived from https://hackmd.io/@lnu-iot/r1aui0B59#Datacake-part

# These variables are specific to me, you will need to change them accordingly
SERIAL_NUMBER = '1234Julia1234'
MQTT_BROKER = 'mqtt.datacake.co'
TOKEN = '48c27ecc04e0671cddb6b426e0cdb73fe065dca9'
PORT = 1883

''' A function which takes in a topic an message and then prints the message.
    Returns nothing'''
def sub_cb(topic, msg):
   print(msg)

# MQTT Setup
client = MQTTClient(SERIAL_NUMBER,
                    MQTT_BROKER,
                    user=TOKEN,
                    password=TOKEN,
                    port=PORT)
client.set_callback(sub_cb)
client.connect()
print('connected to MQTT broker') # If this does not get printed someting is wrong!

#----------------------------------PUBLISH DATA---------------------------------
# The MQTT topic that we publish data to
my_topic_temp = 'dtck-pub/temp-4/992aa037-ba50-4bbc-b67f-c73fc83bb789/TEMPRATURE'
my_topic_cooldown = 'dtck-pub/temp-4/992aa037-ba50-4bbc-b67f-c73fc83bb789/COOLDOWN'

pycom.heartbeat(False)

# Phase 1 is heating
Heating = True
while Heating: # Whilst we heat up the hot tool, get temprature and publish it
    pycom.rgbled(0xFF0000)  # Blink red during this phase
    temp = get_data()
    client.publish(my_topic_temp, msg=str(int(temp)))

    print("Send data to MQTT broker, sleeping for 10 sec...") # Confirmation that we are resing
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
    client.publish(my_topic_temp, msg=str(int(temp)))
    print("Send data to MQTT broker, sleeping for 10 sec...")
    time.sleep(10)
    i += 10 # Add 10 sec to counter (Since we waited 10 since last time)

    # Note: This threshold might be different for different people, play around with it!
    if temp < 36: # Change if needed
        print('cooldown time done: ', i, 'Secs')
        client.publish(my_topic_cooldown, msg=str(int(i))) # Publish this!
        Cooldown = False
#------------------------------------------------------------------------------
