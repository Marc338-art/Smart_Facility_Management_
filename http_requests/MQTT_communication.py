import requests
import paho.mqtt.client as mqtt

import time as t
from datetime import datetime, timedelta
import re


# Lokale Module / Pakete
from .lesson_hours import *
from .HA_req import *
from .URL_encoding import check_timetable
from .thread_management import *
# Konfiguration / Konstanten
from config import MQTT_USER, MQTT_PASS, MQTT_BROKER, MQTT_TOPIC

MQTT_PORT = 1883
MQTT_TOPIC1="ha_main"
MQTT_TOPIC2 = "stundenplan_belegung"
MQTT_TOPIC3 ="wandthermostat_aenderung"  # entweder alle topics in config oder keine







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


# MQTT-Dispatcher Tabelle mit den passenden Funktionen je nach Payload
MQTT_functions = {
    MQTT_TOPIC1: thread_manager,
    MQTT_TOPIC2: lambda _: check_timetable(), # Lambda um Payload zu ignorieren
    MQTT_TOPIC3: check_wandthermostat,
}
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"MQTT Nachricht empfangen: {msg.topic} → {payload}")

    func = MQTT_functions.get(msg.topic)
    if func:
        func(payload)
    else:
        print(f"Kein Handler für Topic {msg.topic} gefunden.")


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

