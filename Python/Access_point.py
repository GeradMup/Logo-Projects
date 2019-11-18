from __future__ import division
from pyModbusTCP.client import ModbusClient
import logging
import csv
import time
from datetime import datetime

#Class for handling all the Modbus Connections
import Modbus

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Get the program started here
if __name__ == '__main__':
    
    #Establish a connection to the fridge Logo 
    fridgeLogo = Modbus.ModbusClass()
    fridgeLogo._connectToLogo("192.168.0.123",503)

    #Establish a connection to the Pyronometer Logo
    pyronometerLogo = Modbus.ModbusClass()
    pyronometerLogo._connectToLogo("146.141.117.20",502)

    # Read Data From the Fridge LOGO
    fridge_register_numbers = [0,1,2]
    fridge_data = fridgeLogo._readData(fridge_register_numbers)       

    # Read Data From Pyronometer LOGO
    pyronometer_register_numbers = [0]
    pyronometer_data = pyronometerLogo._readData(pyronometer_register_numbers) 
    
    # First Check for negative numbers using twos compliments. All pyronometer data is positive
    fridge_data = fridgeLogo.twosCompliment(fridge_data)

    # Do the necessary signal condition
    fridge_gain = 1
    fridge_offset = 0
    fridge_data = fridgeLogo.signalConditioning(fridge_gain, fridge_offset, fridge_data)

    pyronometer_gain = 3.05
    pyronometer_offset = 0
    pyronometer_data = pyronometerLogo.signalConditioning(pyronometer_gain, pyronometer_offset, pyronometer_data)

    print("Pyronometer!")
    for _data in pyronometer_data:
        print(_data)

    print("Fridge Data!")
    for _data in fridge_data:
        print(_data)
        
    # endCounter = 0
    # while True:
    #     fridgeLogo.creatCsvFile()
    #     counter = 0
    #     while True:
    #         fridgeLogo._readData()
    #         fridgeLogo.saveData()
    #         time.sleep(5)
    #         counter += 1
    #         if counter == 10:
    #             break

    #     endCounter += 1
    #     if endCounter == 5:
    #         break