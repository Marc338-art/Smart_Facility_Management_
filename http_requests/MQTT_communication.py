import requests
import paho.mqtt.client as mqtt
import threading
import time as t
from datetime import datetime, timedelta
import re
import sched
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import hashlib
import pytz

# Lokale Module / Pakete
from .lesson_hours import *
from .HA_req import *
from .URL_encoding import *

# Konfiguration / Konstanten
from config import MQTT_USER, MQTT_PASS, MQTT_BROKER, MQTT_TOPIC, THESECRET, USERNAME, PASSWORD

MQTT_PORT = 1883
MQTT_TOPIC2 = "stundenplan_belegung"
MQTT_TOPIC3 ="wandthermostat_aenderung"  # entweder alle topics in config oder keine

# Globale Variablen
motion_status = None  # Status des Bewegungssensors
motion_status_received = threading.Event()  # Event zur Synchronisation

# -----------------------------------------------------------------------------------
# Funktionen zur Thread-Steuerung für Raumsensoren und Temperaturregelung
# -----------------------------------------------------------------------------------

def start_thread(raum_nr):
    """
    Startet einen Überwachungsthread für den gegebenen Raum,
    wenn noch kein Thread aktiv ist und der Raum im Zustand 1 (inaktiv) ist.
    """
    print(f"Thread gestartet für Raum: {raum_nr}")
    

    if rooms_dict[raum_nr]["thread_active"]:
        print(f"Thread für Raum {raum_nr} ist bereits aktiv.")
        return

    if rooms_dict[raum_nr]["state"] == 1:
        abfrage_thread1 = threading.Thread(target=check_condition1_thread, args=(raum_nr,), daemon=True)
        rooms_dict[raum_nr]["thread_active"] = True
        abfrage_thread1.start()


def check_condition1_thread(room_nr):
    """
    Überwacht den Bewegungssensor für den Raum.
    Nach 8 Minuten Wartezeit prüft er Bewegung:
    - Bei Bewegung wird Temperatur auf 21 gesetzt und Zustand auf 2 geändert.
    - Ohne Bewegung wird Temperatur auf 17 gesetzt.
    """
    
    
    room_nrs = room_nr.lower()
    room_nrs=room_nrs.replace(".", "_")
    acttime = datetime.now()
    print(f"Überwache Bewegungssensor: binary_sensor.{room_nrs}")

    while rooms_dict[room_nr]["state"] == 1:
        # Wartezeit von 8 Minuten abwarten
        if datetime.now() - timedelta(minutes=8) > acttime:
            res = get_movement_sensor(f"binary_sensor.bewegungssensor_{room_nrs}")

            if res == "on":
                print("Bewegung erkannt:", res)
                rooms_dict[room_nr]["thread_active"] = False
                act = get_current_lesson()

                if act is None:
                    # Keine aktuelle Stunde, Bewegung ignorieren
                    break
                else:
                    try:
                        change_temperature(f"input_number.heating_temperature_{room_nrs}", 21)
                        rooms_dict[room_nr]["state"] = 2
                        
                        print("Raumstatus aktualisiert:", rooms_dict)
                    except Exception as e:
                        print("Fehler beim Ändern der Temperatur:", e)
                break

            elif res == "off":
                print("Keine Bewegung:", res)
                change_temperature(f"input_number.heating_temperature_{room_nrs}", 17)
                rooms_dict[room_nr]["thread_active"] = False
                break

            print("8 Minuten Wartezeit abgelaufen")

        t.sleep(5)
        print("Thread läuft noch...")


def check_condition2_thread(room_nr):
    """
    Überwacht Bewegung über längeren Zeitraum (30 Minuten).
    - Setzt die Temperatur zurück, wenn keine Bewegung in den letzten 30 Minuten erkannt wurde.
    """
    t.sleep(30 * 60)  # 30 Minuten warten, bis zum Stundenbeginn
    last_active_time = 0
    last_check_time = t.time()

    while True:
        current_time = t.time()
        try:
            res = get_movement_sensor(f"binary_sensor.bewegungssensor_{room_nr}")

            if res == "on" and (last_active_time <= current_time - 8 * 60):
                last_active_time = current_time
                print("Bewegung erkannt")

        except Exception as e:
            print("Exception beim Lesen des Bewegungssensors:", e)

        # Nach 30 Minuten prüfen, ob Bewegung vorhanden war
        if last_check_time <= current_time - 30 * 60:
            room_nrs = room_nr.upper()
            room_nr_upper = room_nrs.replace("_", ".")
            if last_active_time >= last_check_time:
                print("Bewegung innerhalb der letzten 30 Minuten erkannt.")
                rooms_dict[room_nr_upper]["thread_active"] = False
                break
            else:
                print("Keine Bewegung innerhalb der letzten 30 Minuten erkannt.")
                change_temperature(f"input_number.heating_temperature_{room_nr}", 17)
                rooms_dict[room_nr_upper]["thread_active"] = False
                rooms_dict[room_nr_upper]["state"] = 1
                break

        print("Thread aktiv")
        t.sleep(5)


def check_wandthermostat (payload):
    name_part, temp_part = payload.split(":", 1)
    name = name_part.strip()
    print (name)
    match = re.match(r"Wandthermostat_([A-Z]\d{3})(?:_(\d+))?_", name)

    if match:
        raum_nr = match.group(1).lower()
        instanz_nr = match.group(2)
        if instanz_nr:
                entity_id = f"input_number.heating_temperature_{raum_nr}_{instanz_nr}"
        else:
                entity_id = f"input_number.heating_temperature_{raum_nr}"
    else:
        print("Kein gültiger Wandthermostat-Name.")
        return
    temp_str = temp_part.strip().replace("°C", "").strip()
    temperature = float(temp_str)
    
    change_temperature(entity_id, temperature) # hier muss noch ein try und except hin
    


# -----------------------------------------------------------------------------------
# Hauptfunktion zur Verarbeitung von MQTT-Payloads
# -----------------------------------------------------------------------------------

def main(payload):
    """
    Verarbeitet empfangene MQTT-Payloads und startet ggf. den Überwachungsthread.
    """
    print(f"Empfangener Payload: {payload}")

    match = re.match(r"Bewegungssensor_([A-Z]\d{3})_", payload)

    if match:
        print("Raumnummer extrahiert")
        raum_nr = match.group(1)
        start_thread(raum_nr)
    else:
        print("Unbekannter Payload!")


# -----------------------------------------------------------------------------------
# MQTT Callbacks und Client-Setup
# -----------------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    """
    Callback bei erfolgreicher Verbindung mit MQTT-Broker.
    Abonniert relevante Topics.
    """
    print("MQTT verbunden mit Code: " + str(rc))
    if rc == 0:
        client.subscribe(MQTT_TOPIC)   # Haupt-Topic
        client.subscribe(MQTT_TOPIC2)  # Stundenplan-Topic
        client.subscribe(MQTT_TOPIC3)  #abfrage der wandthermostat temperatur
    else:
        print("Fehler beim Verbinden – Code:", rc)


def on_message(client, userdata, msg):
    """
    Callback für empfangene MQTT-Nachrichten.
    Verarbeitet Nachrichten je nach Topic.
    """
    global motion_status

    payload = msg.payload.decode()
    print(f"MQTT Nachricht empfangen: {msg.topic} → {payload}")

    if msg.topic == "ha_main":
        main(payload)
        # motion_status_received.set()
    elif msg.topic == MQTT_TOPIC2:
        check_timetable()

    elif msg.topic == MQTT_TOPIC3:
        check_wandthermostat(payload)
        print("Das ist das neue Topic")


def start_mqtt():
    """
    Startet den MQTT-Client und verbindet sich mit dem Broker.
    """
    global client

    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


# -----------------------------------------------------------------------------------
# Stundenplanprüfung und Temperatursteuerung
# -----------------------------------------------------------------------------------

# Globale Hilfsvariablen
acttime = 0
movement_list = []
move_act = "off"


def check_timetable():
    """
    Prüft den virtuellen Stundenplan, aktualisiert die Belegungsdaten,
    startet ggf. Threads zur Temperaturregelung und setzt Temperaturen.
    """
    base_url1 = "https://www.Virtueller-Stundenplan.de/Reservierung/"

    # Heutiges Datum in 'YYYY-MM-DD'-Format
    today = datetime.today().strftime("%Y-%m-%d")
    print("Heutiges Datum:", today)

    keyphrase_url=base_url1+"RESTHeatGetKeyphrase.php"
    response = requests.get(keyphrase_url,auth=(USERNAME,PASSWORD), verify=False)
    keyphrase_data=response.json()
    my_key=keyphrase_data.get("KeyPhrase")
    tz = pytz.timezone('Europe/Berlin')
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    print("⏰ Timestamp:", timestamp)
    string_to_encrypt = f"{timestamp} {THESECRET} {USERNAME}"
    # ✅ 3. Verschlüsseln
    encrypted = encrypt(string_to_encrypt, my_key)
    url_encoded_key = requests.utils.quote(encrypted)
# ✅ 4. URL für Raumliste
    today = datetime.today().strftime("%Y-%m-%d")
    url = f"{base_url1}RESTHeatRaumStundenplan.php?key={url_encoded_key}&Raum=C%25&Datum={today}"
    #url = base_url1 + f"RESTHeatRaumStundenplan.php?Raum=C%&Datum={today}"

    # Abruf der Belegungsdaten mit Authentifizierung
    response = requests.get(url, auth=(USERNAME, PASSWORD), verify=False)
    current_lesson = get_current_lesson(30)  # Prüfung mit 30 Minuten Vorlaufzeit
    data = response.json()
    print("Stundenplandaten:", data)

    belegung = data.get("Belegung", {})
    #belegung["C005"]=[0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1]

    print("Aktuelle Stunde:", current_lesson)

    for room_name, room_data in rooms_dict.items():
        try:
            # Raum ist im Zustand 1 (inaktiv) und aktuell belegt?
            if ( room_name in belegung):

                raum_name_lower = room_name.lower().replace(".", "_")

                if belegung[room_name][current_lesson] == 1:
                    room_data["state"] = 2

                    # Thread für Überwachung starten
                    abfrage_thread2 = threading.Thread(target=check_condition2_thread, args=(raum_name_lower,), daemon=True)
                    rooms_dict[room_name]["thread_active"] = True
                    abfrage_thread2.start()

                    # Temperatur erhöhen
                    try:
                        change_temperature(f"input_number.heating_temperature_{raum_name_lower}", 24)
                    except Exception as e:
                        print("Fehler beim Temperatursetzen:", e)

                
                elif belegung[room_name][current_lesson]==0 :
                    print("Keine Belegung in der nächsten Stunde")
                    room_data["state"] == 1
                    try:
                        change_temperature(f"input_number.heating_temperature_{raum_name_lower}", 17)
                    except Exception as e:
                        print("Fehler beim Temperatursetzen:", e)


        except Exception:
            print("Keine aktuelle Stunde oder Fehler bei Raumprüfung")


    print("Aktueller Zustand der Räume:", rooms_dict)  # Debugging



    

    