import logging
import requests
import paho.mqtt.client as mqtt
import time as t
from datetime import datetime, timedelta
import re

# Lokale Module / Pakete
from .lesson_hours import *
from .http_req import *
from .URL_encoding import check_timetable
from .thread_management import *

# -----------------------------------------------------------------------------------
# Konfiguration / Konstanten
# -----------------------------------------------------------------------------------

from config import MQTT_USER, MQTT_PASS, MQTT_BROKER, MQTT_TOPIC

MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

MQTT_TOPIC1 = "ha_main"
MQTT_TOPIC2 = "stundenplan_belegung"
MQTT_TOPIC3 = "wandthermostat_aenderung"  # Entweder alle Topics in config oder keine

# -----------------------------------------------------------------------------------
# MQTT Callback-Funktionen
# -----------------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    """
    Callback bei erfolgreicher Verbindung mit MQTT-Broker.
    Abonniert relevante Topics.
    """
    
    
    if rc == 0:
        logging.info("MQTT verbunden mit Code: %s", rc)
        client.subscribe(MQTT_TOPIC)    # Haupt-Topic
        client.subscribe(MQTT_TOPIC2)   # Stundenplan-Updates
        client.subscribe(MQTT_TOPIC3)   # Wandthermostat-Änderungen
    else:
        logging.error("Fehler beim Verbinden – Code: %s", rc)


# Dispatcher-Tabelle für eingehende Nachrichten
MQTT_functions = {
    MQTT_TOPIC1: thread_manager,
    MQTT_TOPIC2: lambda _: check_timetable(),  # Lambda ignoriert Payload
    MQTT_TOPIC3: check_wandthermostat,
}


def on_message(client, userdata, msg):
    """
    Callback bei Empfang einer MQTT-Nachricht.
    Leitet je nach Topic an die passende Funktion weiter.
    """
    payload = msg.payload.decode()
    

    func = MQTT_functions.get(msg.topic)
    if func:
        func(payload)
    else:
        logging.warning("Kein Handler für Topic %s gefunden", msg.topic)


# -----------------------------------------------------------------------------------
# MQTT Startfunktion
# -----------------------------------------------------------------------------------

def start_mqtt():
    """
    Startet den MQTT-Client und verbindet sich mit dem Broker.
    """
    global client

    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    client.loop_forever()
