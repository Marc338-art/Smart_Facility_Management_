import threading
import time
import sched
from http_requests.MQTT_communication import start_mqtt


scheduler = sched.scheduler(time.time, time.sleep)


if __name__ == "__main__":
    
    # startet den MQTT-Client
    start_mqtt()
 





