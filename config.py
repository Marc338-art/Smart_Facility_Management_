from dotenv import load_dotenv
import os

load_dotenv()  # .env wird nur hier einmal geladen

# Alle benötigten Variablen definieren
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
TOKEN = os.getenv("TOKEN")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = os.getenv("MQTT_PORT")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# Stundenplan Abfrage
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
THESECRET = os.getenv("THESECRET")
BASE_URL = os.getenv("BASE_URL")

#Home Assistant URL
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")