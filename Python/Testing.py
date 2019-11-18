import logging
import snap7
import time 
# for setup the Logo connection please follow this link
# http://snap7.sourceforge.net/logo.html

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# make an object for accessing your LOGO!
plc = snap7.logo.Logo()

# TSAP of LOGO: 03.00, TSAP of this Client: 21.00
# must be configured accordingly to settings in LOGO!Soft
# IP-address must be set correctly too
# And now connect
plc.connect("192.168.0.123",0x0300,0x2000)

# if we have a connection...
if plc.get_connected():

    logger.info("connected")
    NI1 = "V0.0" # define virtual input address
    NQ1 = "V3.0" # Virtual Output Variable
    AI3 = "VW0"  # Address for the battery voltage pin
    AI5 = "VW2"  # Address for the Internal Temperature
    AI6 = "VW4"  # Address for the Ambient Temperature
    
    Battery_voltage = plc.read(AI3)/10      # Reading battery voltage
    Internal_Temp = plc.read(AI5)/10        # Reading Internal temperatue
    Ambient_temp = plc.read(AI6)/10         # Reading Ambient Temperature    

    logger.info(Battery_voltage) 
    logger.info(Internal_Temp)
    logger.info(Ambient_temp)
else:
    logger.error("Conncetion failed")

plc.disconnect()
logger.info("Disconnected")
plc.destroy()