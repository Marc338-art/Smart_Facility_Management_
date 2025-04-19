import paho.mqtt.client as mqtt
 
MQTT_BROKER = "172.30.10.212"
MQTT_PORT = 1883
MQTT_TOPIC = "ha_main"
 
MQTT_USER = "mqtt-user"       # dein Benutzername aus HA
MQTT_PASS = "12345678"       # dein Passwort
 
def main(payload):
    print("Zustand 1")
    print(f"Empfangener Payload: {payload}")
 
def on_connect(client, userdata, flags, rc):
    print("MQTT verbunden mit Code: " + str(rc))
    if rc == 0:
        client.subscribe(MQTT_TOPIC)
    else:
        print("Fehler beim Verbinden – Code:", rc)
 
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"MQTT Nachricht empfangen: {msg.topic} → {payload}")
    main(payload)
 
def start_mqtt():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.on_message = on_message
 
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
 
if __name__ == "__main__":
    start_mqtt()