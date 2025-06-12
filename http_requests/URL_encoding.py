import base64
import hashlib
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from datetime import datetime
import pytz


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


