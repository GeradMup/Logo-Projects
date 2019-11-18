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
    
    # Generic Function for reading from any LOGO 
    def _readData(self, _list = [], *args):
        _data = []
        for regNumber in _list:
            dataValue = self._client.read_holding_registers(regNumber)            # Reading voltage on AI3
            dataValue = dataValue[0]
            dataValue = int(dataValue)
            _data.append(dataValue)  
        else:
            return _data
        
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
    def twosCompliment(self, _list, *args):
        _result_list = []
        for number in _list:
            # All values are expected to be below 8 Bits. If More than 8 Bits, number is negative
            if number > 256:
                number = number - 65536
                _result_list.append(number)
            else:
                number = number
                _result_list.append(number)
        else:
            return _result_list

    # Convert the electrical signals into meaningful data
    def signalConditioning(self,_gain, _offset, _signals = [], *args):
        _result_list = []
        for _signal in _signals:
            _conditioned_signal = (_signal*_gain + _offset)/10
            _result_list.append(_conditioned_signal)
        else:
            return _result_list

