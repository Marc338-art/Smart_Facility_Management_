import threading
import time
import sched
import http_requests.MQTT_communication as mqtt_com


scheduler = sched.scheduler(time.time, time.sleep)


if __name__ == "__main__":
    
    # startet den MQTT-Client
    mqtt_com.start_mqtt()
 





