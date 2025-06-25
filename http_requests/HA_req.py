import requests
import time as t
from datetime import datetime, timedelta, time
from .lesson_hours import *
from config import  TOKEN
import re
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import hashlib
import pytz
# Lokale Module / Pakete
from .lesson_hours import *
from .URL_encoding import *

# Basis-URL für Home Assistant API (kann auch aus config geladen werden)
HOME_ASSISTANT_URL = "http://172.30.100.216:8123"

# HTTP Header für Authentifizierung und Content-Type
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}



def get_current_time(delta_t=0):
    """
    Gibt die aktuelle Uhrzeit zurück, optional mit Zeitverschiebung in Minuten.
    
    Args:
        delta_t (int): Anzahl der Minuten, um die die aktuelle Zeit verschoben werden soll (Standard 0).
    
    Returns:
        datetime.time: Aktuelle Uhrzeit (ggf. verschoben).
    """
    now = datetime.now()
    shifted_time = now + timedelta(minutes=delta_t)
    return time(shifted_time.hour, shifted_time.minute)


def get_current_lesson(delta_t=0):
    """
    Bestimmt die aktuelle Unterrichtsstunde anhand der aktuellen Zeit.
    
    Args:
        delta_t (int): Zeitverschiebung in Minuten, um z.B. Vorlaufzeiten zu berücksichtigen (Standard 0).
    
    Returns:
        int oder None: Nummer der aktuellen Stunde oder None, wenn keine Stunde passt.
    """
    current_time = get_current_time(delta_t)
    for stunde in LESSON_HOURS:
        if stunde["start"] <= current_time < stunde["ende"]:
            return stunde["stunde"]
    return None


def change_temperature(entity_id, value=17):
    """
    Ändert den Wert eines input_number-Entities in Home Assistant (z.B. Heiztemperatur).
    
    Args:
        entity_id (str): Entity-ID des input_number (z.B. "input_number.heating_temperature_C001").
        value (float/int): Neuer Wert für das Entity (Standard 17).
    """
    url = f"{HOME_ASSISTANT_URL}/api/services/input_number/set_value"
    data = {"entity_id": entity_id, "value": value}

    try:
        response = requests.post(url, json=data, headers=HEADERS)
        if response.status_code == 200:
            print(f"{entity_id} Temperatur erfolgreich auf {value} gesetzt!")
        else:
            print(f"Fehler beim Setzen der Temperatur ({response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Exception beim HTTP-Request: {e}")



def get_movement_sensor(entity_id):
    """
    Liest den Status eines Bewegungssensors von Home Assistant aus.
    
    Args:
        entity_id (str): Entity-ID des Sensors (z.B. "binary_sensor.bewegungssensor_C001").
    
    Returns:
        str oder None: 'on' oder 'off' wenn erfolgreich, sonst None.
    """
    url = f"{HOME_ASSISTANT_URL}/api/states/{entity_id}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Hebt Fehler hervor, falls HTTP-Status nicht OK
        return response.json()['state']  # Statuswert, z.B. 'on' oder 'off'
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen des Sensorstatus: {e}")
        return None

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
                    rooms_dict[room_name]["state"] = 2

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
                    rooms_dict[room_name]["state"] = 1
                    try:
                        change_temperature(f"input_number.heating_temperature_{raum_name_lower}", 17)
                    except Exception as e:
                        print("Fehler beim Temperatursetzen:", e)


        except Exception:
            print("Keine aktuelle Stunde oder Fehler bei Raumprüfung")


    print("Aktueller Zustand der Räume:", rooms_dict)  # Debugging
