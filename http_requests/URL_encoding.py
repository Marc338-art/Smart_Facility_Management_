import base64
import hashlib
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from datetime import datetime
import pytz
from config import USER, PASSWORD, BASE_URL, THESECRET

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



# ✅ 1. KeyPhrase holen
keyphrase_url = BASE_URL + "RESTHeatGetKeyphrase.php"
response = requests.get(keyphrase_url, auth=(USER, PASSWORD), verify=False)

# Falls du echte Antwort nehmen willst:
keyphrase_data = response.json()
my_key = keyphrase_data.get("KeyPhrase")

# Manuell festgelegt:
#my_key = "e02-89d-59a"

if not my_key:
    print("❌ KeyPhrase konnte nicht geladen werden.")
    exit()

# ✅ 2. Zeichenkette erstellen
tz = pytz.timezone('Europe/Berlin')
timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
print("⏰ Timestamp:", timestamp)

string_to_encrypt = f"{timestamp} {THESECRET} {USER}"

# ✅ 3. Verschlüsseln
encrypted = encrypt(string_to_encrypt, my_key)
url_encoded_key = requests.utils.quote(encrypted)

# ✅ 4. URL für Raumliste
url = f"{BASE_URL}RESTHeatRaumliste.php?key={url_encoded_key}"
print(f"📡 Aufruf-URL: {url}")

# ✅ 5. Anfrage an API
response2 = requests.get(url, auth=(USER, PASSWORD), verify=False)

if response2.status_code != 200:
    print("❌ Fehler:", response2.text)
else:
    print("✅ Antwort von API:\n", response2.text)
