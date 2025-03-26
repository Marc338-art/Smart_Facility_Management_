# Anforderungen

Diese Dokument enthält die Anforderungen an das Python Projekt zum senden der http-Anfragen. Es beschreibt funktionale und nicht funktionale Anforderungen.

## Anforderungen Python-Skript:
### Das Python-Skript muss automatisch auf dem Raspberry Pi laufen.
`req~auto_start~1`
Status: proposed

Description:
Sobald der Raspberry am Strom und eingeschaltet ist, soll das Skript automatisch vom Betriebssystem gestartet werden. Außerdem soll das skript jede nacht um 0 Uhr neu gestartet werden

Needs: doc

### Der Code muss einen request an die Stundenplan-API senden.
`req~tests~1`
Status: proposed

Description:
Es soll eine request an die Stundenplan-URL gesendet werden. Im Header muss ein Token sein um ein Zugriff zu ermöglichen. Außerdem soll als Content-Type "aplication/json" ausgewählt werden und als weiterer Parameter das aktuelle Datum gesendet werden.

Needs: doc

### Der Code muss die Angeforderten Daten temporär speichern.
`req~requirements~1`
Status: proposed

Description:
Der http-request liefert ein JSON-File zurück. Dieser enthält für jeden Raum ein Array mit den Stunden und der Information, ob der Raum für die jeweilige Stunde belegt ist.

Needs: doc

### Der Code muss die Stunden mit einem passenden Uhrzeit-Array abgleichen.
`req~requirements~1`
Status: proposed

Description:
Es muss ein Array erstellt werde, die Schulstunden (1-16) mit der Uhrzeit verknüpft.

Needs: doc

### Der Code muss eine Funktion zum senden von anweisung an Home-Assistant enthalten.
`req~requirements~1`
Status: proposed

Description:
Mit der funktion soll ein http-request an Home-Assistant geschickt werden. Der Request, soll die Daten eines Temperatur-Wertes in der configuration.yaml in Home Assistant auf 21 Grad setzen, wenn der Raum belegt ist. Wenn der Raum nicht belegt ist, soll die Heiztemperatur auf 17 Grad gestellt werden.

Needs: doc

### Der Code soll 15 Minuten vor jeder Unterrichtsstunde prüfen ob der Raum belegt ist.
`req~requirements~1`
Status: proposed

Description:
Es soll 15 Minuten vor jeder Unterrichtsstunde geprüft werden, ob der Raum belegt ist oder nicht je nach Ergebnis soll die Funktion zum setzten der Temperatur mit dem passenden Parameter übergeben werden.

Needs: doc


### Fehlermeldungen bei request sollen abgefangen werden
`req~requirements~1`
Status: proposed

Description:
Beim Aufruf der request-Methode kann es zu Fehlern kommen. Diese Fehler sollen mit Hilfe von try-except-Blöcken abgefangen werden, sodass das Programm nicht abrupt abgebrochen wird. Falls die Anfrage fehlschlägt, soll sie automatisch erneut ausgeführt werden.

Needs: doc

## Anforderungen automation.yaml:

### Die Automation muss auf den Fenstersensor reagieren.
`req~labyrinth-rechteck~1`
Status: proposed

Description:
Sobald der Fenstersensor des jeweiligen Raumes aufgeht (positive Flanke) soll der Sollwert des Heizreglers auf 17 Grad gestellt werden. Solange das Fenster offen ist, darf die Temperatur nicht umgestellt werden. Wenn das Fenster wieder geschlossen wird, soll die Temperatur auf die heating_temperature aus der configuration.yaml gestellt werden.

Needs: arch

### Die Automation muss auf die Heizunsteuerung reagieren
`req~labyrinth-breite~1`
Status: proposed

Description: 
Es muss möglich sein die Temperatur des Raumes über einen Heizungsregler im Raum einzustellen. Die einstellung über den Regler muss höchste Priorität haben und die Temperaturwerte vom Python-Algorithmus überscheiben. Auch bei offenem Fenster soll die Temperatur verändert werden können, aber erst beim schließen des Fenster auch an die Termostate gesendet werden(1 stunde aktiv oder bis die Stunde zuende ist)

### Die Automation muss auf einstellungen vom Layout reagieren
`req~labyrinth-breite~1`
Status: proposed

Description: 
!!hier noch notieren!!
Needs: arch

### backup falls die Stundenplan anbindung nicht funktioniert
`req~labyrinth-laenge~1`
Status: proposed

Description:
Falls es probleme mit dem Zugriff auf die Stundenplan API gibt, muss eine Defaault Automation laufen. In der Dafault Automation kann man die heizung mit den Reglern steuern.
Needs: arch
