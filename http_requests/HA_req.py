import requests
import json
import time as t
from datetime import time
from .lesson_hours import *

# Home Assistant Konfiguration
HOME_ASSISTANT_URL = "http://172.30.10.212:8123"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhODU2YTc1MjhmZGQ0NzdmOTEwZDZhMmM0YmM3ZjRmYiIsImlhdCI6MTc0MDEzMjEyMywiZXhwIjoyMDU1NDkyMTIzfQ."
    "5MjPlnG806hSVln2OUW-LyqP0InyHfPdisiEAd26vTc"
)
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# JSON-Datei laden
with open("data/Belegung neu.JSON", "r") as file:       ## load JSON soll eine Funktion werden
    data_JSON = json.load(file)

# Standardwerte
conditionFlag = 1  # Default-Zustand ist 1
next_lesson = None

def get_current_time():
    """Gibt die aktuelle Uhrzeit zurück."""
    now = t.localtime()
    return time(now.tm_hour, now.tm_min)

def get_current_lesson():
    """Gibt die aktuelle Unterrichtsstunde zurück."""
    current = get_current_time()
    for stunde in LESSON_HOURS:
        if stunde["start"] <= current < stunde["ende"]:
            return stunde["stunde"]
    return None

def change_temperature(entity_id, value=17):
    """Ändert die Temperatur eines Home Assistant Entities."""
    url = f"{HOME_ASSISTANT_URL}/api/services/input_number/set_value"
    data = {"entity_id": entity_id, "value": value}
    response = requests.post(url, json=data, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"{entity_id} Temperatur erfolgreich gesetzt!")
    else:
        print(f"Fehler {response.status_code}: {response.text}")

def get_movement_sensor(entity_id):
    """Überprüft den Zustand des Bewegungssensors."""
    url = f"{HOME_ASSISTANT_URL}/api/states/{entity_id}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Wirft eine Exception bei einem HTTP Fehler
        return response.json()['state']  # 'on' oder 'off'
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen des Sensorstatus: {response.status_code}")
        return None

def activate_script(script_name):
    """Aktiviert ein Home Assistant Script."""
    
    url = f"{HOME_ASSISTANT_URL}/api/services/script/turn_on"
    data = {"entity_id": f"script.{script_name}"}
    try:
        response = requests.post(url, headers=HEADERS, json=data, timeout=10)
        response.raise_for_status()  # Wirft eine Exception bei einem HTTP Fehler
        print(response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Aktivieren des Scripts: {e}")
