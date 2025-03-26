import requests
from .lesson_hours import *
from datetime import time
import time as t


def get_current_time():
    now = t.localtime()
    return time(now.tm_hour, now.tm_min)


def get_current_lesson():
    current = get_current_time()
    for stunde in LESSON_HOURS:
        if stunde["start"] <= current < stunde["ende"]:
            return stunde["stunde"]
    return None  # Falls keine Stunde passt


def get_timetable():
    #hier soll der http-Request zur Stundenplan API gemacht werden
    return None

def check_():
    # hier wird get_current_lesson aufgerufen. der Stunde wir dann mit dem Knüft und der stunde verknüpft.
    
    array_examplehours=[1,1,0,0,0,1,1,1,1,1,1,1,1,1] # nur zum test. Am ende ist dass das ergebniss aus der get_timetable Funktion

    # man kann die aktuelle Stunde als Zahlenwert in den Arrray der Räume packen (array[akt_stunde])
    current_lesson = get_current_lesson()
    if( current_lesson==None):
        change_temperature(ROOMS["C009"]) # erstelle ein array mit allen räumen und der heating temperature für jeden Raumn
        return
    else:
        if(array_examplehours[get_current_lesson()]==1):
            change_temperature(ROOMS["C009"],21) #statt 21 eine constante übergeben
        else:
            change_temperature(ROOMS["C009"])

            ## hier soll eine Flag gestzt werden, um in den Zustand 2 zu kommen.
     

def change_temperature(entity_id, value=17):

    # Home Assistant URL (change to your setup)
    HOME_ASSISTANT_URL = "http://homeassistant.local:8123"

    # Long-Lived Access Token
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhODU2YTc1MjhmZGQ0NzdmOTEwZDZhMmM0YmM3ZjRmYiIsImlhdCI6MTc0MDEzMjEyMywiZXhwIjoyMDU1NDkyMTIzfQ.5MjPlnG806hSVln2OUW-LyqP0InyHfPdisiEAd26vTc"

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
