# hier sind allgemein benöbitgte Funktionen definiert

import requests
from .lesson_hours import *
from datetime import time
import time as t
import json


with open("data/Belegung.JSON", "r") as file:
    data = json.load(file)

conditionFlag=1 #default Zustand ist 1
next_lesson = None
HOME_ASSISTANT_URL = "http://homeassistant.local:8123"

array_examplehours=[1,1,0,0,0,1,1,1,1,1,0,1,0,1,1,0] # nur zum test. Am ende ist dass das ergebniss aus der get_timetable Funktion (die letzte null als puffer damit es in Zustand 0 geht)

    # Long-Lived Access Token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhODU2YTc1MjhmZGQ0NzdmOTEwZDZhMmM0YmM3ZjRmYiIsImlhdCI6MTc0MDEzMjEyMywiZXhwIjoyMDU1NDkyMTIzfQ.5MjPlnG806hSVln2OUW-LyqP0InyHfPdisiEAd26vTc"



def get_current_time():
    now = t.localtime()
    return time(now.tm_hour, now.tm_min)


def get_current_lesson():
    current = get_current_time() # hier muss man noch 30 Minuten addieren, damit es früher ausgelöst wird
    for stunde in LESSON_HOURS:
        if stunde["start"] <= current < stunde["ende"]:
            
            return stunde["stunde"]
    return None  # Falls keine Stunde passt




def change_temperature(entity_id, value=17):

    # Home Assistant URL (change to your setup)
    
    # Headers for authentication
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    url = f"{HOME_ASSISTANT_URL}/api/services/input_number/set_value"
    data = {
        "entity_id": entity_id,
        "value": value
    }
    
    response = requests.post(url, json=data, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"{entity_id} turned on successfully!")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Example usage
#change_temperature("input_number.heating_temperature")#akl


def get_movement_sensor():
    SENSOR_ENTITY_ID = "binary_sensor.hmip_smi55_2_0031a2698ec1ed_bewegung"
    

   
        # Anfrage an die Home Assistant API, um den aktuellen Zustand des Bewegungssensors zu erhalten
    headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }

        # Sende die Anfrage und hole die Sensor-Daten
    response = requests.get(f"{HOME_ASSISTANT_URL}/api/states/{SENSOR_ENTITY_ID}", headers=headers)
        
    if response.status_code == 200:
            state = response.json()['state']  # Der Zustand des Sensors (z.B. 'on' oder 'off')
            return state
                 
    else:
            print(f"Fehler beim Abrufen des Sensorstatus: {response.status_code}")




 
def activate_script():
     
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    SCRIPT_NAME = "heating"
 
    url = f"{HOME_ASSISTANT_URL}/api/services/script/turn_on"
 
    data = {"entity_id": f"script.{SCRIPT_NAME}"}
 
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.text)