from __future__ import division
from pyModbusTCP.client import ModbusClient
import logging
import time

#Class for handling all the Modbus Connections
import Modbus

#Class for handling all the data storage related tasks
import Data_Storage

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Get the program started here
if __name__ == '__main__':
    
    #Establish a connection to the fridge Logo 
    fridgeLogo = Modbus.ModbusClass()
    fridge_ip = "146.141.117.21"
    fridge_port = 502
    fridgeLogo._connectToLogo(fridge_ip, fridge_port)

    #Establish a connection to the Pyronometer Logo
    pyronometerLogo = Modbus.ModbusClass()
    pyronometer_ip = "146.141.117.20"
    pyronometer_port = 502
    pyronometerLogo._connectToLogo(pyronometer_ip, pyronometer_port)

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

    pyronometer_gain = 1
    pyronometer_offset = 0
    pyronometer_data = pyronometerLogo.signalConditioning(pyronometer_gain, pyronometer_offset, pyronometer_data)

    print("Pyronometer!")
    for _data in pyronometer_data:
        print(_data)

    print("Fridge Data!")
    for _data in fridge_data:
        print(_data)

    # Create a list for data storage format
    _data_to_save = [fridge_data[0],fridge_data[1],fridge_data[2],pyronometer_data[0]]

    #Save the captured data
    _file_name = "Fridge_Pyronometer_Data"
    _headers = ['Battery Voltage (V)','Internal Temperature (^o C)','External Temperature (^o C)','Irradiance (W/m^2)']
    
    _data_store = Data_Storage.StorageClass()
    _data_store.creatCsvFile(_file_name,_headers)
    _data_store.saveData(_data_to_save)

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