import requests
import paho.mqtt.client as mqtt
import threading
import time
from datetime import datetime, timedelta
from .lesson_hours import *
from .HA_req import *
import sched
import re

# MQTT-Konfiguration
MQTT_BROKER = "172.30.100.216"
MQTT_PORT = 1883
MQTT_TOPIC = "ha_main"
MQTT_USER = "mqtt-user"  # dein Benutzername aus HA
MQTT_PASS = "12345678"  # dein Passwort



HOME_ASSISTANT_URL = "http://172.30.100.216:8123"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjMzRjYzM4Y2M4Zjc0Y2VjYTY2ZWE1YTdlYmY5ZTAzMyIsImlhdCI6MTc0ODI0ODU1MiwiZXhwIjoyMDYzNjA4NTUyfQ.76QdyxQOibfPOg-6cFvMSpEWr-nwAl67pzBhzm2zNV8"
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
    if rooms_dict[raum_nr]["thread_active"]:
        print(f"Thread für Raum {raum_nr} ist bereits aktiv.")
        return
    if rooms_dict[raum_nr]["state"]==1:  
        
        abfrage_thread1 = threading.Thread(target=check_condition1_thread, args=(room_nr,), daemon=True)
        rooms_dict[room_nr]["thread_active"]=True
        abfrage_thread1.start()


def check_condition1_thread(room_nr):
    acttime = datetime.now()
    
    print(f"binary_sensor.{room_nr}")
    while rooms_dict[room_nr]["state"]==1:
        
        
        if datetime.now() - timedelta(minutes=10) > acttime:

            res=get_movement_sensor(f"binary_sensor.bewegungssensor_{room_nr}")
            if res =="on":
                print(res)
                rooms_dict[room_nr]["thread_active"]=False
                change_temperature(f"input_number.heating_temperature_{room_nr}",21)
                rooms_dict[room_nr]["state"]=2
                # hier soll noch das Ende der aktuellen Stunde rein, da dann aufgehört werden soll zu heizen
                break

            elif res =="off":
                print(res)
                change_temperature(f"input_number.heating_temperature_{room_nr}",17)
                rooms_dict[room_nr]["thread_active"]=False
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
            res=get_movement_sensor(f"binary_sensor.bewegungssensor_{room_nr}")

            if res == "on" and (last_active_time <= current_time - 8*60): # nach 8 minuten wird geprüft 
                last_active_time = current_time  # Aktualisiere die letzte Aktivität
                print("Bewegung erkannt")

        except:
            print("Exception")
            
            

        if  last_check_time <= current_time - 30*60:
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
