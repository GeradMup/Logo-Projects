import os
import numpy
import pandas as pd
import sys
import datetime
import time
import gzip
import shutil
from datetime import timezone

#os.chdir(r'C:\Users\Wits\Desktop\Pyranometer Data')

rawDataFolder = r'C:\Users\Wits\Desktop\RawData'
formattedDataFolder = r'C:\Users\Wits\Desktop\formatedData'
archivedDataFolder = r'C:\Users\Wits\Desktop\archivedData'

try:
    os.makedirs(formattedDataFolder)
    os.makedirs(archivedDataFolder)
except OSError:
    if not os.path.isdir(formattedDataFolder):
        raise
    if not os.path.isdir(archivedDataFolder):
        raise
os.chdir(rawDataFolder)  
    
allfiles = []
allfiles = os.listdir()

# Read_in the csv file
for files in allfiles:
    os.chdir(rawDataFolder)
    data = pd.read_csv(allfiles[0], sep =',')
    os.chdir(formattedDataFolder)
    serialNumber = files[:-4]

'''
List of metrices:
                *** MinimumIrradiance
                    MaximumIrradiance
                    AvarageIrradiance
                    StandardDeviation
'''

metrics = ['MinimumIrradiance', 'AvarageIrradiance', 'MaximumIrradiance', 'StandardDeviation']




for metric in metrics:
        fileName = str(serialNumber + metric)
        outFile = open(fileName, 'w')
        newline = ''
        for cell in range(0,data.shape[0]):
            # Timestamp
            originalDate = data.iloc[cell,0]
            year = originalDate[0:4]
            month = originalDate[6:7]
            day = originalDate[8:10]
            hour = originalDate[11:13]
            minute = originalDate[14:16]
                

            timeToDatetime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
            unixTimestamp = int(timeToDatetime.replace(tzinfo = timezone.utc).timestamp())

            # Defining the magnitude value
            metricNumber = metrics.index(metric) + 2
            magnitude = data.iloc[cell, metricNumber]
            

            # Creating and adding the tags
            serialNumberTag = 'SerialNumber=' + str(serialNumber)
            minimumIrradianceTag = 'Min_Irradiance=' + str(data.iloc[cell,2])
            maximumIrradianceTag = 'Max_Irradiance=' + str(data.iloc[cell,3])
            avarageIrradianceTag = 'Avg_Irradiance=' + str(data.iloc[cell,4])
            standardDeviationTag = 'Standard_Div=' + str(data.iloc[cell, 5])

             
            # An identifier should be created so that the system can be identified as a solar unit or a battery unit
            unitTypeTag = 'UnitType=' + 'Solar_Irrad_Sensor'
            
            line = newline + str(metric) + ' ' + str(unixTimestamp) + ' ' + str(magnitude) + ' ' + serialNumberTag + ' '+ unitTypeTag
            outFile.write(line)
            
            # Redefine \n so that you do not have a newline character at the end of the file created
            newline = '\n'

        outFile.close()

        # Zip all files
        fileNameZipped = fileName + '.gz'
        with open(fileName, 'rb') as f_in:
            with gzip.open(fileNameZipped, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        # Intermediate files are removed as only the zipped files are required
        os.remove(fileName)

        # Archived file should contain the date and time range, this will make the files unique

#'''
