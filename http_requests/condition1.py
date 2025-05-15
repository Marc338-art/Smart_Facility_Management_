# Hier ist der Code gespeichert, der im Zustand 1 benötigt wird
# Dieser Code steuert die Heizungsregelung basierend auf Stundenplan- und Bewegungssensordaten.
# Wenn eine Unterrichtsstunde erkannt wird, wird die Temperatur angepasst.
# Falls der Raum nicht belegt ist, aber Bewegung erkannt wird, kann temporär geheizt werden.

from . import HA_req

# Globale Variablen
acttime = 0
movement_list = []
move_act = "off"

def get_timetable():
    """Hier soll der HTTP-Request zur Stundenplan-API gemacht werden."""
    try:
        # Hier sollte der eigentliche Request zur Stundenplan-API erfolgen
        return None  
    except Exception as e:
        print(f"Fehler beim Abrufen des Stundenplans: {e}")
        return None

def check_():
    """Prüft die aktuelle Unterrichtsstunde und setzt die Temperatur entsprechend."""
    try:
        current_lesson = HA_req.get_current_lesson()
    
        if current_lesson is None:
            HA_req.change_temperature(HA_req.ROOMS["C005"])  # Temperatur nur bei Änderung setzen
            return
        
        if HA_req.data_JSON["Belegung"]["A001"][0][current_lesson - 1] == 1:  # -1, da keine Stunde 0 existiert
            HA_req.change_temperature(HA_req.ROOMS["C005"], 21)  # Statt 21 könnte eine Konstante genutzt werden
            
            # Setze next_lesson für spätere Verwendung
            HA_req.next_lesson = current_lesson - 1  
            
            # Zustand setzen: Raum ist belegt und wird geheizt
            HA_req.conditionFlag = 2
        else:
            HA_req.change_temperature(HA_req.ROOMS["C005"])  # Standardtemperatur setzen
    
    except Exception as e:
        print(f"Fehler in check_(): {e}")

def check_movement_Zustand1(entity_id):
    """Prüft, ob Bewegung erkannt wurde, obwohl der Raum nicht belegt ist."""
    global acttime, movement_list, move_act
    c_time = HA_req.t.time()
    
    try:
        move_act = HA_req.get_movement_sensor(entity_id)
        print(move_act)
        print(acttime)
    
        if move_act == "on" and acttime <= c_time - 10 * 60:  # Alle 10 Minuten Sensor auslesen
            acttime = HA_req.t.time()
            movement_list.append(move_act)
            print("Bewegung erkannt")
            return
        
        if len(movement_list) == 2:
            print("Aktiviere Skript")
            try:
                HA_req.activate_script()
            except Exception as e:
                print(f"Fehler beim Aktivieren des Skripts: {e}")
            movement_list.clear()
        
        # Heizung nur für 30 Minuten aktiv halten
        elif len(movement_list) == 1 and acttime <= c_time - 20 * 60:  # Innerhalb 15 Min keine zweite Bewegung → Zurücksetzen
            print("Keine zweite Bewegung, setze Skript zurück")
            movement_list.clear()
    
    except Exception as e:
        print(f"Fehler in check_movement_Zustand1(): {e}")

    return
