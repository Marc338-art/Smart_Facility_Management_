import requests
import paho.mqtt.client as mqtt
import threading
import time as t
from datetime import datetime, timedelta
from .lesson_hours import *
from .HA_req import *
from . import condition1 as c1
import sched
import re
from config import MQTT_USER, MQTT_PASS, TOKEN, HOME_ASSISTANT_URL, MQTT_BROKER, MQTT_TOPIC, THESECRET,USERNAME, PASSWORD, BASE_URL


from . import HA_req
from . import lesson_hours as lh
import main as sat
import threading as thr



MQTT_PORT = 1883

MQTT_TOPIC2="stundenplan_belegung"

HOME_ASSISTANT_URL = "http://172.30.100.216:8123"
'''TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjMzRjYzM4Y2M4Zjc0Y2VjYTY2ZWE1YTdlYmY5ZTAzMyIsImlhdCI6MTc0ODI0ODU1MiwiZXhwIjoyMDYzNjA4NTUyfQ.76QdyxQOibfPOg-6cFvMSpEWr-nwAl67pzBhzm2zNV8"
)'''
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
    room_nrs=room_nr.replace(".", "_")
    if rooms_dict[raum_nr]["thread_active"]:
        print(f"Thread für Raum {raum_nr} ist bereits aktiv.")
        return
    elif rooms_dict[raum_nr]["state"]==1:  
        
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
            
        t.sleep(5)
        print("Thread läuft noch")

def check_condition2_thread(room_nr):
    last_active_time = 0
    last_check_time = t.time()  
    
    while True:
        current_time = t.time()
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
                rooms_dict[room_nr]["thread_active"]=False
                break
            else:
                print("Keine Bewegung innerhalb der letzten 30 Minuten erkannt.")
                change_temperature(f"input_number.heating_temperature_{room_nr}",17)
                rooms_dict[room_nr]["thread_active"]=False
                rooms_dict[room_nr]["state"]=1
                break
                # Hier kann der Zustand weiter verarbeitet werden
            
        print("thread aktiv")
        t.sleep(5)




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
        client.subscribe(MQTT_TOPIC2)  # Abonniere ha_main Topic
    
    else:
        print("Fehler beim Verbinden – Code:", rc)

# Callback für eingehende MQTT-Nachrichten
def on_message(client, userdata, msg):
    global motion_status
    payload = msg.payload.decode()
    print(f"MQTT Nachricht empfangen: {msg.topic} → {payload}")
    
    # Wenn die Antwort auf den Bewegungssensor empfangen wird
    if msg.topic == "ha_main":
        main(payload)
        #motion_status_received.set()  # Signalisiere, dass die Antwort angekommen ist
    elif msg.topic== MQTT_TOPIC2:
        check_timetable()
        
    

# Startet den MQTT-Client und verbindet sich mit dem Broker
def start_mqtt():
    global client

    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

#import http_requests as http
# Globale Variablen
acttime = 0
movement_list = []
move_act = "off"


def check_timetable():
    print("BASE_URL:", repr(BASE_URL))
    print("USERNAME:", repr(USERNAME))
    print("PASSWORD:", repr(PASSWORD))
    base_url1 = "https://www.Virtueller-Stundenplan.de/Reservierung/"
# ✅ 1. KeyPhrase holen
    today = datetime.today().strftime("%Y-%m-%d")
    print("Heutiges Datum:", today)
    url = base_url1 + f"RESTHeatRaumStundenplan.php?Raum=C%&Datum={today}"
    #url = BASE_URL + "RESTHeatRaumStundenplan.php?Raum=C0%&Datum=2025-04-02"
    response = HA_req.requests.get(url, auth=(USERNAME, PASSWORD), verify=False)
    current_lesson =HA_req.get_current_lesson() # gibt nur einen Wert wenn keine pause ist. (einbauen das geprüft wird falls None) ## es soll aber immer 30 Minuten vorher geschaut werden, welche Stunde in 30 Minuten ist
    data = response.json()
    print(data)
    belegung = data.get("Belegung", {})
    belegung["C005"]=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    print (current_lesson)

    for room_name, room_data in rooms_dict.items():
        try:
            if room_data["state"] == 1 and room_name in belegung and belegung[room_name][current_lesson]==1 :    ## Funktion fragt stundenplan ab und schaut ob die aktuelle stunde Blegt ist oder nicht. falls ja, schaut sie bis der Raum belegt ist und bestimmt einen Endzeitpunkt. Soll
                raum_name=room_name.lower() # doppelt sich mit der lower funktion unten
                raum_name=room_name.replace(".", "_")
                room_data["state"] = 2
                abfrage_thread2 = thr.Thread(target=check_condition2_thread, args=(raum_name,), daemon=True)
                rooms_dict[room_name]["thread_active"] = True
                abfrage_thread2.start()
              
                # hier soll thread 1 gestoppt werden, wenn er noch aktiv ist

                room_name_s=room_name.lower()
                r_s=room_name_s.replace(".", "_")
                try:
                    change_temperature(f"input_number.heating_temperature_{r_s}",24)
                    print(r_s)
                except :
                    print("mistake")
                for index in range(current_lesson + 1, len(belegung[room_name])):
                    h = belegung[room_name][index]
                    if h == 0:
                        print(f"Raum frei ab Stunde {index }")
                        try:
                            stunden_ende = LESSON_HOURS[index-2]["ende"]
                            room_data["end_time"] = stunden_ende
                            print(f"Ende der Stunde {index }: {stunden_ende.strftime('%H:%M')}")
                        except IndexError:
                            print(f"Kein Eintrag in LESSON_HOURS für Index {index}")
                        break  # Nur den nächsten freien Slot finden
        except:
            print("aktuell keine sutnde")                   

        if room_data["state"] == 2 and room_name in belegung:
            if room_data["end_time"] and get_current_time() > room_data["end_time"]:
                # Temperatur zurücksetzen
                print(f"Temperatur in {room_name} wird zurückgesetzt (Zeit ist abgelaufen).")
                room_name_s=room_name.lower()
                r_s=room_name_s.replace(".", "_")

                # Hier kannst du z. B. einen Service aufrufen:
                room_data["state"] = 1
                try:
                    change_temperature(f"input_number.heating_temperature_{r_s}",17)
                except :
                    print("mistake")
    

