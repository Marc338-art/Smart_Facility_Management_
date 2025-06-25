import base64
import hashlib
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from datetime import datetime
import pytz


from .lesson_hours import *

def encrypt(string, secret_key):
    key = hashlib.sha256(secret_key.encode()).digest()[:32]
    aesgcm = AESGCM(key)
    import os
    iv = os.urandom(12)  # ✅ korrekt für 96-bit (12 Byte) IV
 # generates 12 bytes for IV
    nonce = iv  # synonym für IV bei AES-GCM

    string_bytes = string.encode('utf-8')
    tag_length = 16  # GCM standard
    ciphertext = aesgcm.encrypt(nonce, string_bytes, None)  # ciphertext + tag
    encrypted_data = nonce + ciphertext  # append IV + ciphertext+tag

    return base64.b64encode(encrypted_data).decode('utf-8')


def check_timetable():
    """
    Prüft den virtuellen Stundenplan, aktualisiert die Belegungsdaten,
    startet ggf. Threads zur Temperaturregelung und setzt Temperaturen.
    """
    base_url1 = "https://www.Virtueller-Stundenplan.de/Reservierung/"

    # Heutiges Datum in 'YYYY-MM-DD'-Format
    today = datetime.today().strftime("%Y-%m-%d")
    print("Heutiges Datum:", today)

    keyphrase_url=base_url1+"RESTHeatGetKeyphrase.php"
    response = requests.get(keyphrase_url,auth=(USERNAME,PASSWORD), verify=False)
    keyphrase_data=response.json()
    my_key=keyphrase_data.get("KeyPhrase")
    tz = pytz.timezone('Europe/Berlin')
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    print("⏰ Timestamp:", timestamp)
    string_to_encrypt = f"{timestamp} {THESECRET} {USERNAME}"
    # ✅ 3. Verschlüsseln
    encrypted = encrypt(string_to_encrypt, my_key)
    url_encoded_key = requests.utils.quote(encrypted)
# ✅ 4. URL für Raumliste
    today = datetime.today().strftime("%Y-%m-%d")
    url = f"{base_url1}RESTHeatRaumStundenplan.php?key={url_encoded_key}&Raum=C%25&Datum={today}"
    #url = base_url1 + f"RESTHeatRaumStundenplan.php?Raum=C%&Datum={today}"

    # Abruf der Belegungsdaten mit Authentifizierung
    response = requests.get(url, auth=(USERNAME, PASSWORD), verify=False)
    current_lesson = get_current_lesson(30)  # Prüfung mit 30 Minuten Vorlaufzeit
    data = response.json()
    print("Stundenplandaten:", data)

    belegung = data.get("Belegung", {})
    #belegung["C005"]=[0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1]

    print("Aktuelle Stunde:", current_lesson)

    for room_name, room_data in rooms_dict.items():
        try:
            # Raum ist im Zustand 1 (inaktiv) und aktuell belegt?
            if ( room_name in belegung):

                raum_name_lower = room_name.lower().replace(".", "_")

                if belegung[room_name][current_lesson] == 1:
                    rooms_dict[room_name]["state"] = 2

                    # Thread für Überwachung starten
                    abfrage_thread2 = threading.Thread(target=check_condition2_thread, args=(raum_name_lower,), daemon=True)
                    rooms_dict[room_name]["thread_active"] = True
                    abfrage_thread2.start()

                    # Temperatur erhöhen
                    try:
                        change_temperature(f"input_number.heating_temperature_{raum_name_lower}", 24)
                    except Exception as e:
                        print("Fehler beim Temperatursetzen:", e)

                
                elif belegung[room_name][current_lesson]==0 :
                    print("Keine Belegung in der nächsten Stunde")
                    rooms_dict[room_name]["state"] = 1
                    try:
                        change_temperature(f"input_number.heating_temperature_{raum_name_lower}", 17)
                    except Exception as e:
                        print("Fehler beim Temperatursetzen:", e)


        except Exception:
            print("Keine aktuelle Stunde oder Fehler bei Raumprüfung")


    print("Aktueller Zustand der Räume:", rooms_dict)  # Debugging

