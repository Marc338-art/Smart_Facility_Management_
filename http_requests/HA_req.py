import requests

import time as t
from datetime import datetime, timedelta, time
from .lesson_hours import *
from config import  TOKEN

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
    #url = f"{HOME_ASSISTANT_URL}/api/services/input_number/set_value"
    url = f"{HOME_ASSISTANT_URL}/api/services/climate/set_temperature
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

