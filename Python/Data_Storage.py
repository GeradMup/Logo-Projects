import csv
import time
from datetime import datetime

class StorageClass:

    # Create the file for saving data. Each file is created with a time stamp of when it was created
    def creatCsvFile(self, _file_name, _headers):
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        time = now.strftime("%Hh%M")

        self.fileName = _file_name + year + '.' + month + '.' + day + "_" + time + ".csv"
        self.fileName = str(self.fileName)

        with open(self.fileName ,'w',newline='') as newFile:
            _myWriter = csv.writer(newFile)
            _myWriter.writerow(_headers)

    # Save the data
    def saveData(self, _data):
        with open(self.fileName,'a',newline='') as _file:
            _myWriter = csv.writer(_file)
            _myWriter.writerow(_data)
        pass
