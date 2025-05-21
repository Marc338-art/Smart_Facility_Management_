import requests
import paho.mqtt.client as mqtt
import threading
import time
from datetime import datetime, timedelta
import sched
import http_requests as http
import re
# MQTT-Konfiguration
MQTT_BROKER = "172.30.10.212"
MQTT_PORT = 1883
MQTT_TOPIC = "ha_main"
MQTT_USER = "mqtt-user"  # dein Benutzername aus HA
MQTT_PASS = "12345678"  # dein Passwort


scheduler = sched.scheduler(time.time, time.sleep)

HOME_ASSISTANT_URL = "http://172.30.10.212:8123"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhODU2YTc1MjhmZGQ0NzdmOTEwZDZhMmM0YmM3ZjRmYiIsImlhdCI6MTc0MDEzMjEyMywiZXhwIjoyMDU1NDkyMTIzfQ."
    "5MjPlnG806hSVln2OUW-LyqP0InyHfPdisiEAd26vTc"
)
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


motion_status = None  # Variable, um den Status des Bewegungssensors zu speichern
motion_status_received = threading.Event()  # Event, um die Antwort zu synchronisieren

# Beispiel-Funktionen, die je nach Payload ausgeführt werden
def start_thread(raum_nr):

    print(f"Thread gestartet für Raum: {raum_nr}")
    room_nr=raum_nr
    room_nrs=room_nr.lower()
    if http.rooms_dict[raum_nr]["thread_active"]:
        print(f"Thread für Raum {raum_nr} ist bereits aktiv.")
        return
    if http.rooms_dict[raum_nr]["state"]==1:  
        
        abfrage_thread1 = threading.Thread(target=check_condition1_thread, args=(room_nr,), daemon=True)
        http.rooms_dict[room_nr]["thread_active"]=True
        abfrage_thread1.start()

    '''elif  http.rooms_dict[raum_nr]["state"]==2:
        abfrage_thread = threading.Thread(target=check_condition2_thread, args=(room_nr,), daemon=True)
        http.rooms_dict[room_nr]["thread_active"]=True
        abfrage_thread.start()'''

def check_condition1_thread(room_nr):
    acttime = datetime.now()
    
    print(f"binary_sensor.{room_nr}")
    while http.rooms_dict[room_nr]["state"]==1:
        # Überprüfe alle 30 Sekunden, ob 12 Minuten vergangen sind
        
        if datetime.now() - timedelta(minutes=10) > acttime:

            res=http.get_movement_sensor(f"binary_sensor.bewegungssensor_{room_nr}")
            if res =="on":
                print(res)
                http.rooms_dict[room_nr]["thread_active"]=False
                http.change_temperature(f"input_number.heating_temperature_{room_nr}",21)
                http.rooms_dict[room_nr]["state"]=2
                break

            elif res =="off":
                print(res)
                http.change_temperature(f"input_number.heating_temperature_{room_nr}",17)
                http.rooms_dict[room_nr]["thread_active"]=False
                break

            print("Zeit abgelaufen")
            
        time.sleep(5)
        print("Thread läuft noch")

def check_condition2_thread(room_nr):
    last_active_time = 0
    last_check_time = time.time()  
    
    while True:
        current_time = time.time()
        try:
            res=http.get_movement_sensor(f"binary_sensor.bewegungssensor_{room_nr}")
        except:
            print("Exception")

        if res == "on" and (last_active_time <= current_time - 60):
            last_active_time = current_time  # Aktualisiere die letzte Aktivität
            print("Bewegung erkannt")
            
            

        if  last_check_time <= current_time - 2*60:
            room_nr=room_nr.upper()
            if last_active_time >= last_check_time:
                print("Bewegung innerhalb der letzten 30 Minuten erkannt.")
                http.rooms_dict[room_nr]["thread_active"]=False
                break
            else:
                print("Keine Bewegung innerhalb der letzten 30 Minuten erkannt.")
                http.change_temperature(f"input_number.heating_temperature_{room_nr}",17)
                http.rooms_dict[room_nr]["thread_active"]=False
                http.rooms_dict[room_nr]["state"]=1
                break
                # Hier kann der Zustand weiter verarbeitet werden
            
        print("thread aktiv")
        time.sleep(5)




# Hauptfunktion, die abhängig vom Payload aufruft
def main(payload):
    print(f"Empfangener Payload: {payload}")
    match = re.match(r"Bewegungssensor_([A-Z]\d{3})_", payload)
    
    if match:
        print("Raumnummerübertragen")
        raum_nr = match.group(1)  # z. B. "c009"
        start_thread(raum_nr)
    else:
        print("Unbekannter Payload!")

# Callback für die MQTT-Verbindung
def on_connect(client, userdata, flags, rc):
    print("MQTT verbunden mit Code: " + str(rc))
    if rc == 0:
        # Abonniere beide relevanten Topics
        client.subscribe(MQTT_TOPIC)  # Abonniere ha_main Topic
    
    else:
        print("Fehler beim Verbinden – Code:", rc)

# Callback für eingehende MQTT-Nachrichten
def on_message(client, userdata, msg):
    global motion_status
    payload = msg.payload.decode()
    print(f"MQTT Nachricht empfangen: {msg.topic} → {payload}")
    
    # Wenn die Antwort auf den Bewegungssensor empfangen wird
    if msg.topic == "home/response/motion_status":
        motion_status = payload  # Den erhaltenen Status speichern
        print(f"Status des Bewegungssensors empfangen: {motion_status}")
        motion_status_received.set()  # Signalisiere, dass die Antwort angekommen ist

    main(payload)

# Startet den MQTT-Client und verbindet sich mit dem Broker
def start_mqtt():
    global client

    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

 
def schedule_task():
    scheduler.run()
    # Plane die nächste Ausführung der main-Funktion in 20 Sekunden
    scheduler.enter(5*60, 1, schedule_task)  # Wiederhole alle 5 Sekunden
    print(http.rooms)
    http.check_timetable()



if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()

    # Starte den Scheduler in einem eigenen Thread
    schedule_task()
    # Starte die Ausführung des Schedulers
    scheduler.run()

    '''while True:
        for i in range (1,1000):
            if i==3000:
                print(i)'''

