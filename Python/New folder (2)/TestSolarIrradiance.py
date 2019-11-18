from pyModbusTCP.client import ModbusClient
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

_client = ModbusClient()
minimum = "global"
maximum = "global"
avarage = "global"
logger.info("connecting")

# Connect to LOGO
try:
    _client.host("146.141.117.20")
    _client.port(503)
    _client.open()
    logger.info("connected")
except ValueError:
    logger.info("Failed To Connect")

