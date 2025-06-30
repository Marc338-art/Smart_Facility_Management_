# Smart Facility Management

Das Projekt bildet die zentrale Steuereinheit eines smarten Raumsteuerungssystems. Über MQTT-Nachrichten und HTTP-Requests werden Informationen ausgetauscht, um auf Basis von Stundenplänen, Sensorwerten und Belegungsdaten die Temperatur in Räumen automatisch zu regulieren. Der Raspberry Pi fungiert hierbei als Kommunikationszentrale zwischen Home Assistant, Stundenplandatenbank und Raumhardware.

## 🔧 Projektstruktur

Das Projekt ist in mehrere Module unterteilt:

- ``\
  Initialisiert Raumzustände basierend auf Stundenplandaten. Jeder Raum erhält einen Default-Zustand mit `state = 1` (nicht belegt) und `thread_active = False`.

- ``\
  Enthält Funktionen zur Kommunikation mit Home Assistant über HTTP. Hierüber können z. B. Bewegungssensoren abgefragt oder Raumtemperaturen gesetzt werden.

- ``\
  Beinhaltet die Funktion `check_timetable()`, welche mit AES-GCM verschlüsselte Anfragen an die Stundenplandatenbank stellt. Erkennt sie bevorstehenden Unterricht, wird die Temperatur auf 21 °C gesetzt und ein Überprüfungsthread gestartet.

- ``\
  Verwaltet die MQTT-Verbindung und implementiert eine dispatcher-basierte Steuerung je nach empfangenem Topic.

- ``\
  Enthält die Logik zur Steuerung paralleler Threads, etwa zur Prüfung von Bewegungen vor und während des Unterrichts. Reagiert auf reale Raumbelegung und passt die Temperatur an.

## 💡 Ziel

Energieeffiziente, belegungsabhängige Steuerung von Raumtemperaturen mithilfe von Planungs- und Sensordaten – ohne übermäßige Zusatzhardware wie Fensterkontakte oder Bewegungsmelder.

## 📌 Hinweis

Das Repository ist erreichbar unter:\
**[Link zum GitLab-Repo einfügen]**

## ✨ Installation

1. Repository klonen:

   ```bash
   git clone https://gitlab.gwdg.de/m.schroeder07/smart_facility_management.git
   cd smart_facility_management
   ```

2. Virtuelle Umgebung erstellen und aktivieren:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Abhängigkeiten installieren:

   ```bash
   pip install -r requirements.txt
   ```

4. Konfigurationsdatei (`config.py`) anlegen und Zugangsdaten für MQTT, URLs etc. eintragen.

5. Programm starten:

   ```bash
   python main.py
   ```

