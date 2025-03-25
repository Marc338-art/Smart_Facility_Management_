# Anforderungen

Diese Dokument enthält die Anforderungen an das Python Projekt zum senden der http-Anfragen. Es beschreibt funktionale und nicht funktionale Anforderungen.

## Anforderungen Python-Skript:
### Das Python-Skript muss automatisch auf dem Raspberry Pi laufen.
`req~auto_start~1`
Status: proposed

Description:
Sobald der Raspberry am Strom und eingeschaltet ist, soll das Skript automatisch vom Betriebssystem gestartet werden.

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

## Anforderungen automation.yaml:

### Das Labyrinth muss ein Recheck abbilden.
`req~labyrinth-rechteck~1`
Status: proposed

Description:
Das Labyrinth für dieses Programm ist rechteckig.
Es begrenzt den Bereich in dem der Spieler sich bewegen kann auftreten kann.
Die Einschraenkung auf ein Rechteck erleichtert die spaetere Verarbeitung erheblich.

Needs: arch

### Die Breite des Labyrinths muss ermittelt werden.
`req~labyrinth-breite~1`
Status: proposed

Description:
Die Breite des Labyrinths muss bekannt sein.
Die Breite legt die Größe des Labyrinths in horizontaler Richtung fest.
Die Breite begrenzt den Bereich, in dem der Spieler sich in horizontaler Richtung bewegen kann.

Needs: arch

### Die Länge des Labyrinths muss ermittelt werden.
`req~labyrinth-laenge~1`
Status: proposed

Description:
Die Länge des Labyrinths muss bekannt sein.
Die Länge legt die Größe des Labyrinths in vertikaler Richtung fest.
Die Länge begrenzt den Bereich, in dem der Spieler sich in vertikaler Richtung bewegen kann.

Needs: arch

### Der Spieler muss im Labyrinth bleiben.
`req~spieler-innerhalb-labyrinth~1`
Status: proposed

Description:
Der Spieler darf das Labyrinth nicht verlassen.
Die Position des Spielers muss immer innerhalb der Außenmauern des Labyrinths sein.
Verlässt der Spieler das Labyrinth, kann er es nicht mehr erfolgreich durchlaufen.

Needs: arch

### Der Eingang des Labyrinths muss ermittelt werden.
`req~labyrinth-eingang~1`
Status: proposed

Description:
Der Eingang des Labyrinths muss bekannt sein.
Der Eingang ist gleichzeitig die Startposition des Spielers.
Die Kenntnis über den Eingang ist notwendig, um jede weitere Position des Spielers zu ermitteln.

Needs: arch

### Der Ausgang des Labyrinths muss ermittelt werden.
`req~labyrinth-ausgang~1`
Status: proposed

Description:
Der Ausgang des Labyrinths muss bekannt sein.
Der Ausgang des Labyrinths stellt gleichzeitig das Ziel des Spielers dar.
Erreicht der Spieler den Ausgang, wurde das Labyrinth erfolgreich durchlaufen.
Die Kenntnis über den Ausgang ist notwendig, um das Programm im richtigen Moment zu beenden.

Needs: arch

### Die aktuelle Position des Spielers muss ermittelt werden.
`req~aktuelle-position-spieler~1`
Status: proposed

Description:
Die aktuelle Position des Spielers muss bekannt sein.
Die aktuelle Position hängt von der Startposition sowie allen vorausgegangenen Schritten ab.
Der nächste Schritt hängt von der aktuellen Position ab.
Die aktuelle Position muss nach jedem Schritt neu ermittelt werden.

Needs: arch

### Die direkt Umgebung des Spielers muss ermittelt werden.
`req~umgebung-spieler~1`
Status: proposed

Description:
Die Umgebung des Spielers muss bekannt sein.
Die direkte Umgebung besteht aus mindestens einem Feld in jede Richtung, also aus acht Feldern.
Ist die direkte Umgebung nicht bekannt, ist es nicht möglich zu entscheiden, wo der Spieler sinnvoller Weise als nächstes hingeht.

Needs: arch

### Wände müssen unüberwindbar für den Spieler sein.
`req~waende-unueberwindbar~1`
Status: proposed

Description:
Der Spieler darf nicht durch Wände gehen oder sie überspringen.
Die Wände schränken die Bewegung des Spielers ein.
Die Unüberwindbarkeit der Wände stellt sicher, dass der Spieler das Labyrinth nicht verlässt.

Needs: arch

### Der Spieler muss sich nach unten bewegen.
`req~spieler-bewegung-unten~1`
Status: proposed

Description:
Der Spieler muss sich nach unten bewegen.
Der Schritt nach unten ist notwendig, um das Ziel zu erreichen.
Die Bewegung nach unten hängt von der aktuellen Position, der direkten Umgebung des Spielers und der ausgewählten Lösungsstrategie ab.

Needs: arch

### Der Lösungsalgorithmus muss sich beenden wenn der Spieler das Ziel erreicht.
`req~loesungsalgorithmus-beendet~1`
Status: proposed

Description:
Der Lösungsalgorithmus muss sich beenden, sobald der Spieler das Ziel erreicht.
Stimmt die aktuelle Position mit dem Ausgang des Labyrinths überein, wurde das Labyrinth erfolgreich durchlaufen.
Das Beenden des Lösungsalgorythmus verhindert die endlose Laufzeit des Programms.

Needs: arch