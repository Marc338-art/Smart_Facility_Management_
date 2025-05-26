
import threading
import time
import sched
import http_requests.MQTT_communication as mqtt_com
import http_requests.condition1 as req

scheduler = sched.scheduler(time.time, time.sleep)
def schedule_task():
    scheduler.run()
    # Plane die nächste Ausführung der main-Funktion in 20 Sekunden
    scheduler.enter(5*60, 1, schedule_task)  # Wiederhole alle 5 Sekunden
    
    req.check_timetable()



if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=mqtt_com.start_mqtt, daemon=True)
    mqtt_thread.start()

    # Starte den Scheduler in einem eigenen Thread
    schedule_task()
    # Starte die Ausführung des Schedulers
    scheduler.run()


