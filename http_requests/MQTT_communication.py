import requests
import paho.mqtt.client as mqtt
import threading
import time
from datetime import datetime, timedelta
# MQTT-Konfiguration
MQTT_BROKER = "172.30.10.212"
MQTT_PORT = 1883
MQTT_TOPIC = "ha_main"
MQTT_USER = "mqtt-user"  # dein Benutzername aus HA
MQTT_PASS = "12345678"  # dein Passwort


HOME_ASSISTANT_URL = "http://172.30.10.212:8123"
TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhODU2YTc1MjhmZGQ0NzdmOTEwZDZhMmM0YmM3ZjRmYiIsImlhdCI6MTc0MDEzMjEyMywiZXhwIjoyMDU1NDkyMTIzfQ."
    "5MjPlnG806hSVln2OUW-LyqP0InyHfPdisiEAd26vTc"
)
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


motion_status = None  # Variable, um den Status des Bewegungssensors zu speichern
motion_status_received = threading.Event()  # Event, um die Antwort zu synchronisieren

# Beispiel-Funktionen, die je nach Payload ausgeführt werden
def start_thread():
    print("Thread wird gestartet")
    abfrage_thread = threading.Thread(target=check_list_thread, daemon=True)
    abfrage_thread.start()

def check_list_thread():
    acttime = datetime.now()
    
    while True:
        # Überprüfe alle 30 Sekunden, ob 12 Minuten vergangen sind
        if datetime.now() - timedelta(seconds=40) > acttime:

            res=get_movement_sensor("binary_sensor.hmip_smi_00091d8994556f_bewegung")
            if res =="on":
                print(res)
                break

            elif res =="off":
                print(res)
                break

            print("Zeit abgelaufen")
            
        time.sleep(5)
        print("Thread läuft noch")



def tuerkontakt_aktion():
    print("Führe Türkontakt-Aktion aus!")

def wandthermostat_aktion():
    print("Führe Wandthermostat-Aktion aus!")

# Hauptfunktion, die abhängig vom Payload aufruft
def main(payload):
    print(f"Empfangener Payload: {payload}")
    
    if payload == "binary_sensor.hmip_swdm_2_0034a2698f4da2":
        tuerkontakt_aktion()
        start_thread()
    elif payload == "climate.wandthermostat":
        wandthermostat_aktion()
    elif payload == "binary_sensor.hmip_smi_00091d8994556f_bewegung":
        start_thread()
    else:
        print("Unbekannter Payload!")

# Callback für die MQTT-Verbindung
def on_connect(client, userdata, flags, rc):
    print("MQTT verbunden mit Code: " + str(rc))
    if rc == 0:
        # Abonniere beide relevanten Topics
        client.subscribe(MQTT_TOPIC)  # Abonniere ha_main Topic
    
    else:
        print("Fehler beim Verbinden – Code:", rc)

# Callback für eingehende MQTT-Nachrichten
def on_message(client, userdata, msg):
    global motion_status
    payload = msg.payload.decode()
    print(f"MQTT Nachricht empfangen: {msg.topic} → {payload}")
    
    # Wenn die Antwort auf den Bewegungssensor empfangen wird
    if msg.topic == "home/response/motion_status":
        motion_status = payload  # Den erhaltenen Status speichern
        print(f"Status des Bewegungssensors empfangen: {motion_status}")
        motion_status_received.set()  # Signalisiere, dass die Antwort angekommen ist

    main(payload)

# Startet den MQTT-Client und verbindet sich mit dem Broker
def start_mqtt():
    global client

    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


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



if __name__ == "__main__":
    start_mqtt()



