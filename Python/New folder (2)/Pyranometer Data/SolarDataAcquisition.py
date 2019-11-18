from pyModbusTCP.client import ModbusClient
from datetime import datetime, timedelta
from time import strftime
import numpy as np
import schedule
import os.path
import datetime
import time
import sys
import csv

# Global variables
_client = ModbusClient()
_headers = ['Start(South African Standard Time)', 'Stop(South African Standard Time)', 'min_Irradance(W/m^2)',
            'max_Irradance(W/m^2)', 'avarage_Irradance(W/m^2)', 'Standard deviation']

datalist = []


# Connect to LOGO
def InitialiseModbusCommunication():
    try:
        _client.host("146.141.117.20")
        _client.port(504)
        _client.open()
    except AttributeError:
        print("Cannot connect to LOGO!")

    return


"""
Read values from Holding registers and store into a list
"""


def ReadFromModbus():
    irradiance = repr(_client.read_holding_registers(0))
    irradiance = irradiance[1:-1]
    irradiance = int(irradiance)
    datalist.append(irradiance)

    return


'''
Use data stored into a list and take out, the min, max, average and standard deviation
'''


def ModbusTransfer():
    try:

        file_exists = os.path.isfile(CreateNewLogFile())
       
        #print(time.mktime(t.timetuple()), _client.read_holding_registers(0))
        with open(CreateNewLogFile(), "a") as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=_headers)
            if not file_exists:
                writer.writeheader()
            else:
                writer.writerow({'Start(South African Standard Time)': StartTime(),
                                 'Stop(South African Standard Time)': StopTime(),
                                 'min_Irradance(W/m^2)': min(datalist),
                                 'max_Irradance(W/m^2)': max(datalist),
                                 'avarage_Irradance(W/m^2)': ("%.2f" % np.mean(datalist)),
                                 'Standard deviation': ("%.2f" % np.std(datalist))})

    except AttributeError:
        print("Something Wrong with Logging to file!")

    datalist.clear()

    return


'''
Start time and stop time functions 
'''


def StartTime():
    nowtime = datetime.datetime.now() - timedelta(minutes=1)
    #nowtime = nowtime.strftime("%Y-%m-%d %H:%M")
    return nowtime


def StopTime():
    _nowTime = strftime("%Y-%m-%d %H:%M:S")
    return _nowTime


'''
This is to enable the program to Log single file every time interval
'''


def CreateNewLogFile():
    # The program will Log data every day, new set of data will be logged the following day
    _filename = 'DataLog_' + str(datetime.datetime.now().strftime('%Y_%m_%d')) + '.csv'

    return _filename


InitialiseModbusCommunication()

# Schedule a logging interval
schedule.every(1).minutes.do(ModbusTransfer)

# Program runs in a loop
while True:
    ReadFromModbus()
    t = StartTime()
    print(time.mktime(t.timetuple())) 
    schedule.run_pending()
    time.sleep(0)
