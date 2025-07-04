import logging
import threading
import time as t
from datetime import datetime, timedelta
import re

# Lokale Module / Pakete
from .lesson_hours import *
from .http_req import get_movement_sensor, change_temperature, get_current_lesson


# -----------------------------------------------------------------------------------
# Konfiguration & Konstanten
# -----------------------------------------------------------------------------------

WAIT_TIME_MINUTES = 8         # Zeit für Bewegungssensorprüfung in Minuten
CHECK_INTERVAL_SECONDS = 30    # Intervall zwischen Threadprüfungen
NO_MOTION_TEMP = 17           # Temperatur bei keiner Bewegung
MOTION_TEMP = 21              # Temperatur bei Bewegung
LESSON_START_DELAY = 30 * 60  # Wartezeit vor Stundenbeginn in Sekunden


# -----------------------------------------------------------------------------------
# Globale Variablen
# -----------------------------------------------------------------------------------

motion_status = None
motion_status_received = threading.Event()


# -----------------------------------------------------------------------------------
# Funktionen zur Thread-Steuerung für Raumsensoren und Temperaturregelung
# -----------------------------------------------------------------------------------

def start_thread(raum_nr, instanz_nr):
    """
    Startet einen Überwachungsthread für den gegebenen Raum,
    wenn noch kein Thread aktiv ist und der Raum im Zustand 1 (inaktiv) ist.
    """
    
    if instanz_nr:
        raum_nr = f"{raum_nr}.{instanz_nr}"
       

    if rooms_dict[raum_nr]["thread_active"]:
        # Thread für Raum {raum_nr} ist bereits aktiv.
        return

    if rooms_dict[raum_nr]["state"] == 1:
        abfrage_thread1 = threading.Thread(target=check_condition1_thread, args=(raum_nr,), daemon=True)
        rooms_dict[raum_nr]["thread_active"] = True
        abfrage_thread1.start()


def check_condition1_thread(room_nr):
    """
    Überwacht den Bewegungssensor für den Raum.
    Nach WAIT_TIME_MINUTES prüft er Bewegung:
    - Bei Bewegung wird Temperatur auf MOTION_TEMP gesetzt und Zustand auf 2 geändert.
    - Ohne Bewegung wird Temperatur auf NO_MOTION_TEMP gesetzt.
    """
    room_nrs = room_nr.lower().replace(".", "_")
    acttime = datetime.now()
    

    while rooms_dict[room_nr]["state"] == 1:
        if datetime.now() - timedelta(minutes=WAIT_TIME_MINUTES) > acttime:
            res = get_movement_sensor(f"binary_sensor.bewegungssensor_{room_nrs}")

            if res == "on":
                print("Bewegung erkannt:", res)
                rooms_dict[room_nr]["thread_active"] = False
                act = get_current_lesson()

                if act is None:
                    break  # Keine aktuelle Stunde, Bewegung ignorieren
                try:
                    change_temperature(f"input_number.heating_temperature_{room_nrs}", MOTION_TEMP)
                    rooms_dict[room_nr]["state"] = 2
                    
                except Exception as e:
                    logging.error(f"Fehler beim Ändern der Temperatur: {e}")
                break

            elif res == "off":
                
                change_temperature(f"input_number.heating_temperature_{room_nrs}", NO_MOTION_TEMP)
                rooms_dict[room_nr]["thread_active"] = False
                break

            

        t.sleep(CHECK_INTERVAL_SECONDS)
        


def check_condition2_thread(room_nr):
    """
    Überwacht Bewegung über längeren Zeitraum (30 Minuten).
    - Setzt die Temperatur zurück, wenn keine Bewegung erkannt wurde.
    """
    t.sleep(LESSON_START_DELAY)
    last_active_time = 0
    last_check_time = t.time()

    while True:
        current_time = t.time()
        try:
            res = get_movement_sensor(f"binary_sensor.bewegungssensor_{room_nr}")
            if res == "on" and (last_active_time <= current_time - WAIT_TIME_MINUTES * 60):
                last_active_time = current_time
               
        except Exception as e:
            logging.error(f"Fehler beim Lesen des Bewegungssensors: {e}")

        if last_check_time <= current_time - LESSON_START_DELAY:
            room_nrs = room_nr.upper()
            room_nr_upper = room_nrs.replace("_", ".")

            if last_active_time >= last_check_time:
                
                rooms_dict[room_nr_upper]["thread_active"] = False
            else:
                
                change_temperature(f"input_number.heating_temperature_{room_nr}", NO_MOTION_TEMP)
                rooms_dict[room_nr_upper]["thread_active"] = False
                rooms_dict[room_nr_upper]["state"] = 1
            break

        
        t.sleep(CHECK_INTERVAL_SECONDS)


# -----------------------------------------------------------------------------------
# Hauptfunktion zur Verarbeitung von MQTT-Payloads
# -----------------------------------------------------------------------------------

def thread_manager(payload):
    """
    Verarbeitet empfangene MQTT-Payloads und startet ggf. den Überwachungsthread.
    """
    

    match = re.match(r"Bewegungssensor_([A-Z]\d{3})(?:_(\d+))?", payload)

    if match:
        raum_nr = match.group(1)
        instanz_nr = match.group(2)
        
        try:
            start_thread(raum_nr, instanz_nr)
        except Exception as e:
            logging.error(f"Fehler beim Starten des Threads: {e}")
    else:
        logging.warning("Unbekannter Payload empfangen – keine Aktion durchgeführt.")
