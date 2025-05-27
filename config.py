from dotenv import load_dotenv
import os

load_dotenv()  # .env wird nur hier einmal geladen

# Alle benötigten Variablen definieren
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
MQTT_TOKEN = os.getenv("MQTT_TOKEN")

# Stundenplan Abfrage
USER = os.getenv("USER")
PASSWORD= os.getenv("PASSWORD")
THESECRET = os.getenv("THESECRET")
BASE_URL = os.getenv("BASE_URL")