# Hier ist der Code gespeichert, der im Zustand 1 benötigt wird
# Dieser Code steuert die Heizungsregelung basierend auf Stundenplan- und Bewegungssensordaten.
# Wenn eine Unterrichtsstunde erkannt wird, wird die Temperatur angepasst.
# Falls der Raum nicht belegt ist, aber Bewegung erkannt wird, kann temporär geheizt werden.

from . import HA_req
from . import lesson_hours as lh
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


def check_timetable():
    user = "smanemann@bbs2wob-lis.de"
    password = "Wob2HeatTestInitial"
    thesecret = "hPRbaYgljaZCfdTXdGik"
    
    base_url = "https://www.Virtueller-Stundenplan.de/Reservierung/"
 
# ✅ 1. KeyPhrase holen
    url = base_url + "/RESTHeatRaumStundenplan.php?Raum=A0%&Datum=2025-04-02"
    response = HA_req.requests.get(url, auth=(user, password), verify=False)
    current_lesson =HA_req.get_current_lesson() # gibt nur einen Wert wenn keine pause ist. (einbauen das geprüft wird falls None) ## es soll aber immer 30 Minuten vorher geschaut werden, welche Stunde in 30 Minuten ist
    data = response.json()
    belegung = data.get("Belegung", {})
    print (current_lesson)

    for room_name, room_data in lh.rooms_dict.items():
        if room_data["state"] == 1 and room_name in belegung and belegung[room_name][current_lesson]==0 :    ## Funktion fragt stundenplan ab und schaut ob die aktuelle stunde Blegt ist oder nicht. falls ja, schaut sie bis der Raum belegt ist und bestimmt einen Endzeitpunkt. Soll
            room_data["state"] = 2

            for index in range(current_lesson + 1, len(belegung[room_name])):
                h = belegung[room_name][index]
                if h == 0:
                    print(f"Raum frei ab Stunde {index }")
                    try:
                        stunden_ende = HA_req.LESSON_HOURS[index-2]["ende"]
                        room_data["end_time"] = stunden_ende
                        print(f"Ende der Stunde {index }: {stunden_ende.strftime('%H:%M')}")
                    except IndexError:
                        print(f"Kein Eintrag in LESSON_HOURS für Index {index}")
                    break  # Nur den nächsten freien Slot finden


        elif room_data["state"] == 2 and room_name in belegung:
            if room_data["end_time"] and HA_req.get_current_time() > room_data["end_time"]:
                # Temperatur zurücksetzen
                print(f"Temperatur in {room_name} wird zurückgesetzt (Zeit ist abgelaufen).")
                # Hier kannst du z. B. einen Service aufrufen:
                # set_temperature(room_name, default_temp)
    print(lh.rooms_dict)