import base64
import logging
import hashlib
import requests
import os
from datetime import datetime
import pytz
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Lokale Module / Pakete
from .http_req import *
from .lesson_hours import *
from .thread_management import *
from config import TOKEN, THESECRET, USERNAME, PASSWORD

# -----------------------------------------------------------------------------------
# Konstanten
# -----------------------------------------------------------------------------------

BASE_URL = "https://www.Virtueller-Stundenplan.de/Reservierung/"
DEFAULT_TEMP = 17
ACTIVE_TEMP = 24
KEYPHRASE_ENDPOINT = "RESTHeatGetKeyphrase.php"
TIMETABLE_ENDPOINT = "RESTHeatRaumStundenplan.php"
ROOM_PATTERN = "C%25"
TIMEZONE = 'Europe/Berlin'
GCM_TAG_LENGTH = 16
GCM_NONCE_SIZE = 12
LESSON_LOOKAHEAD_MIN = 30


# -----------------------------------------------------------------------------------
# Verschlüsselung
# -----------------------------------------------------------------------------------

def encrypt(string, secret_key):
    key = hashlib.sha256(secret_key.encode()).digest()[:32]
    aesgcm = AESGCM(key)
    nonce = os.urandom(GCM_NONCE_SIZE)
    string_bytes = string.encode('utf-8')

    ciphertext = aesgcm.encrypt(nonce, string_bytes, None)
    encrypted_data = nonce + ciphertext

    return base64.b64encode(encrypted_data).decode('utf-8')


# -----------------------------------------------------------------------------------
# Hauptfunktion: Stundenplanprüfung
# -----------------------------------------------------------------------------------

def check_timetable():
    """
    Prüft den virtuellen Stundenplan, aktualisiert die Belegungsdaten,
    startet ggf. Threads zur Temperaturregelung und setzt Temperaturen.
    """

    # Heutiges Datum
    today = datetime.today().strftime("%Y-%m-%d")
    

    # Keyphrase abrufen
    keyphrase_url = BASE_URL + KEYPHRASE_ENDPOINT
    response = requests.get(keyphrase_url, auth=(USERNAME, PASSWORD), verify=False)
    keyphrase_data = response.json()
    my_key = keyphrase_data.get("KeyPhrase")

    # Zeitstempel für Signatur
    tz = pytz.timezone(TIMEZONE)
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    

    string_to_encrypt = f"{timestamp} {THESECRET} {USERNAME}"
    encrypted = encrypt(string_to_encrypt, my_key)
    url_encoded_key = requests.utils.quote(encrypted)

    # Raumplan-URL zusammensetzen
    timetable_url = (
        f"{BASE_URL}{TIMETABLE_ENDPOINT}?key={url_encoded_key}"
        f"&Raum={ROOM_PATTERN}&Datum={today}"
    )

    # Belegungsdaten abrufen
    response = requests.get(timetable_url, auth=(USERNAME, PASSWORD), verify=False)
    data = response.json()
    belegung = data.get("Belegung", {})
    

    # Aktuelle Stunde mit Vorlauf
    current_lesson = get_current_lesson(LESSON_LOOKAHEAD_MIN)
    

    for room_name, room_data in rooms_dict.items():
        try:
            if room_name in belegung:
                raum_name_lower = room_name.lower().replace(".", "_")

                if belegung[room_name][current_lesson] == 1:
                    rooms_dict[room_name]["state"] = 2

                    abfrage_thread2 = threading.Thread(
                        target=check_condition2_thread,
                        args=(raum_name_lower,),
                        daemon=True
                    )
                    rooms_dict[room_name]["thread_active"] = True
                    abfrage_thread2.start()

                    try:
                        change_temperature(
                            f"input_number.heating_temperature_{raum_name_lower}",
                            ACTIVE_TEMP
                        )
                    except Exception as e:
                        logging.error(f"Fehler beim Temperatursetzen: {e}")

                elif belegung[room_name][current_lesson] == 0:
                    
                    rooms_dict[room_name]["state"] = 1

                    try:
                        change_temperature(
                            f"input_number.heating_temperature_{raum_name_lower}",
                            DEFAULT_TEMP
                        )
                    except Exception as e:
                        logging.error(f"Fehler beim Temperatursetzen: {e}")

        except Exception:
            logging.exception("Keine aktuelle Stunde oder Fehler bei Raumprüfung")

   
