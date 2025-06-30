import logging
import requests
import time as t
from datetime import datetime, timedelta, time
import re
import base64
import hashlib
import pytz
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Lokale Module
from .lesson_hours import *
from config import TOKEN, THESECRET, USERNAME, PASSWORD

# -----------------------------------------------------------------------------------
# Konstanten & Konfiguration
# -----------------------------------------------------------------------------------

HOME_ASSISTANT_URL = "http://172.30.100.216:8123"
DEFAULT_TEMPERATURE = 17
REQUEST_TIMEOUT = 10

# HTTP Header für Home Assistant API
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# -----------------------------------------------------------------------------------
# Zeitfunktionen
# -----------------------------------------------------------------------------------

def get_current_time(delta_t=0):
    """
    Gibt die aktuelle Uhrzeit zurück, optional mit Zeitverschiebung in Minuten.
    """
    now = datetime.now()
    shifted_time = now + timedelta(minutes=delta_t)
    return time(shifted_time.hour, shifted_time.minute)


def get_current_lesson(delta_t=0):
    """
    Bestimmt die aktuelle Unterrichtsstunde anhand der aktuellen Zeit.
    """
    current_time = get_current_time(delta_t)
    for stunde in LESSON_HOURS:
        if stunde["start"] <= current_time < stunde["ende"]:
            return stunde["stunde"]
    return None

# -----------------------------------------------------------------------------------
# Home Assistant API-Funktionen
# -----------------------------------------------------------------------------------

def change_temperature(entity_id, value=DEFAULT_TEMPERATURE):
    """
    Ändert den Wert eines input_number-Entities in Home Assistant.
    """
    url = f"{HOME_ASSISTANT_URL}/api/services/input_number/set_value"
    data = {"entity_id": entity_id, "value": value}

    try:
        response = requests.post(url, json=data, headers=HEADERS)
        if response.status_code == 200:
            logging.info(f"{entity_id}: Temperatur erfolgreich auf {value}°C gesetzt.")
        else:
            logging.error(f"Fehler beim Setzen der Temperatur ({response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Exception beim HTTP-Request: {e}")


def get_movement_sensor(entity_id):
    """
    Liest den Status eines Bewegungssensors von Home Assistant aus.
    """
    url = f"{HOME_ASSISTANT_URL}/api/states/{entity_id}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get('state')
    except requests.exceptions.RequestException as e:
        logging.error(f"Fehler beim Abrufen des Sensorstatus: {e}")
        return None

# -----------------------------------------------------------------------------------
# Wandthermostat-Verarbeitung
# -----------------------------------------------------------------------------------

def check_wandthermostat(payload):
    """
    Verarbeitet ein Payload-String vom Wandthermostat im Format:
    "Wandthermostat_C001_1_: 22.5°C"
    """
    name_part, temp_part = payload.split(":", 1)
    name = name_part.strip()
    

    match = re.match(r"Wandthermostat_([A-Z]\d{3})(?:_(\d+))?", name)
    if match:
        raum_nr = match.group(1).lower()
        instanz_nr = match.group(2)
        if instanz_nr:
            entity_id = f"input_number.heating_temperature_{raum_nr}_{instanz_nr}"
        else:
            entity_id = f"input_number.heating_temperature_{raum_nr}"
    else:
        logging.warning("Kein gültiger Wandthermostat-Name im Payload.")
        return

    try:
        temp_str = temp_part.strip().replace("°C", "").strip()
        temperature = float(temp_str)
        change_temperature(entity_id, temperature)
    except Exception:
        logging.error(f"Wandthermostat-Verarbeitung fehlgeschlagen: {e}")
