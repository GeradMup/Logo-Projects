import pysftp

myhost = "146.141.16.82"
myuser = "labproj"
mypass = "t0ps3cr3t"

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with pysftp.Connection(host=myhost, username=myuser, password=mypass, cnopts = cnopts) as sftp:

    sftp.cwd('OpenTSDB_Data/FormattedData')
    localPath = r'C:\Users\Wits\Desktop\formatedData\pyranometer1StandardDeviation.gz'
    remotePath = 'pyranometer1StandardDeviation.gz'

    #sftp.put(localPath, remotePath)

    

    
