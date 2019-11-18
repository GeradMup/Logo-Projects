from __future__ import division
from pyModbusTCP.client import ModbusClient
import logging
import csv
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class ModbusClass:
    def __init__(self):
        
        # Make an instance of modbus object
        self._client = ModbusClient()

    #Connect to the LOGO
    def _connectToLogo(self,ip_address,port_num):
        try:
            print('Trying to make a connection')
            self._client.host(ip_address)
            self._client.port(port_num)
            self._client.open()
            print('Connected')
        
        except AttributeError:
            print('Failed to connect to Logo')

    #Read data from the LOGO I/O pins
    def _readData(self):
        self.voltage = self._client.read_holding_registers(0)            # Reading voltage on AI3
        self.voltage = self.voltage[0]
        self.voltage = int(self.voltage)        # Convert string to an integer

        self.internalTemp = self._client.read_holding_registers(1)      # Reading upper temperature on AI6
        self.internalTemp = self.internalTemp[0]
        self.internalTemp = int(self.internalTemp)

        self.externalTemp = self._client.read_holding_registers(2)       # Reading ambient temperature on AI5
        self.externalTemp = self.externalTemp[0]
        self.externalTemp = int(self.externalTemp)

        # Perform two's compliment on the 16 Bit number because it is a negative value
        self.voltage = self.twosCompliment(self.voltage)
        self.internalTemp = self.twosCompliment(self.internalTemp)
        self.externalTemp = self.twosCompliment(self.externalTemp)

        # Devide by 10 --> Correct representation of the values
        self.voltage = self.voltage/10
        self.externalTemp = self.externalTemp/10
        self.internalTemp = self.internalTemp/10
        
        print("Voltage: ",self.voltage)
        print("Internal Temperature: ", self.internalTemp)
        print("External Temperature: ", self.externalTemp)
    
    # Generic Function for reading from any LOGO 
    def _readData(self, _list = [], *args):
        for regNumber in _list:
            print(regNumber)
        
    def creatCsvFile(self):
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        time = now.strftime("%Hh%M")

        self.fileName = "Fridge_Data_" + year + '.' + month + '.' + day + "_" + time + ".csv"
        self.fileName = str(self.fileName)

    #    with open(self.fileName ,'w',newline='') as newFile:
    #        _myWriter = csv.writer(newFile)
    #        _myWriter.writerow(['Battery Voltage','Internal Temperature','External Temperature'])

    def saveData(self):
    #    with open(self.fileName,'a',newline='') as _file:
    #        _myWriter = csv.writer(_file)
    #        _myWriter.writerow([self.voltage,self.internalTemp,self.externalTemp])
        pass
    # Perform two's compliment on any given number just incase the number is negative
    def twosCompliment(self,number):
        if number > 256:
            number = number - 65536
        else:
            number = number
        return number

    def disconnect(self):
        pass

# Get the program started here
if __name__ == '__main__':
    
    #Establish a connection to the fridge Logo 
    fridgeLogo = ModbusClass()
    fridgeLogo._connectToLogo("192.168.0.123",503)

    #Establish a connection to the Pyronometer Logo
    pyronometerLogo = ModbusClass()
    pyronometerLogo._connectToLogo("146.141.117.20",502)

    fridge_register_numbers = [0,1,2]
    fridgeLogo._readData(fridge_register_numbers)       # Read Data From the Fridge LOGO
    

    pyronometer_register_numbers = [0]
    pyronometerLogo._readData(pyronometer_register_numbers)
    
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