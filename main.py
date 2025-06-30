import time
import logging
from logging.handlers import RotatingFileHandler

from http_requests.MQTT_communication import start_mqtt


handler = RotatingFileHandler('raum_ueberwachung.log', maxBytes=5*1024*1024, backupCount=3)
# maxBytes = 5 MB, backupCount = 3 Dateien werden aufgehoben

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[handler]
)



if __name__ == "__main__":
    
    # startet den MQTT-Client
    start_mqtt()
 





