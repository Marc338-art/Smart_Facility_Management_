import requests
import json
import time as t
from datetime import time
from datetime import datetime, timedelta, time
from .lesson_hours import *
from config import HOME_ASSISTANT_URL, TOKEN

HOME_ASSISTANT_URL = "http://172.30.100.216:8123"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3ZGMyMDkwMmQ1Mzg0ODE3OTgyZTMyMzc0MDJhNDUzOSIsImlhdCI6MTc0ODkzMDk3OCwiZXhwIjoyMDY0MjkwOTc4fQ.5arpkQnXBm_678tJHsLPzBTLnCe5RT-ZkK2AGwGYtzo"
)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}




# Standardwerte
conditionFlag = 1  # Default-Zustand ist 1
next_lesson = None

def get_current_time(delta_t=0):
    """Gibt die aktuelle Uhrzeit zurück."""
    now = datetime.now()
    new_time = now + timedelta(minutes=delta_t)
    return time(new_time.hour, new_time.minute)

def get_current_lesson(delta_t=0):
    """Gibt die aktuelle Unterrichtsstunde zurück."""
    current = get_current_time(delta_t)
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



