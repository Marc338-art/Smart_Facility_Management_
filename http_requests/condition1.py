# Hier ist der Code gespeichert, der im Zustand 1 benötigt wird
# Dieser Code steuert die Heizungsregelung basierend auf Stundenplan- und Bewegungssensordaten.
# Wenn eine Unterrichtsstunde erkannt wird, wird die Temperatur angepasst.
# Falls der Raum nicht belegt ist, aber Bewegung erkannt wird, kann temporär geheizt werden.

from . import HA_req
from . import lesson_hours as lh
import main as sat
#import http_requests as http
# Globale Variablen
acttime = 0
movement_list = []
move_act = "off"


def check_timetable():
    user = "smanemann@bbs2wob-lis.de"
    password = "Wob2HeatTestInitial"
    thesecret = "hPRbaYgljaZCfdTXdGik"
    
    base_url = "https://www.Virtueller-Stundenplan.de/Reservierung/"
 
# ✅ 1. KeyPhrase holen
    url = base_url + "/RESTHeatRaumStundenplan.php?Raum=C0%&Datum=2025-04-02"
    response = HA_req.requests.get(url, auth=(user, password), verify=False)
    current_lesson =HA_req.get_current_lesson() # gibt nur einen Wert wenn keine pause ist. (einbauen das geprüft wird falls None) ## es soll aber immer 30 Minuten vorher geschaut werden, welche Stunde in 30 Minuten ist
    data = response.json()
    belegung = data.get("Belegung", {})
    print (current_lesson)

    for room_name, room_data in lh.rooms_dict.items():
        try:
            if room_data["state"] == 1 and room_name in belegung and belegung[room_name][current_lesson]==1 :    ## Funktion fragt stundenplan ab und schaut ob die aktuelle stunde Blegt ist oder nicht. falls ja, schaut sie bis der Raum belegt ist und bestimmt einen Endzeitpunkt. Soll
                raum_name=room_name.lower() # doppelt sich mit der lower funktion unten
                room_data["state"] = 2
                abfrage_thread2 = sat.threading.Thread(target=sat.check_condition2_thread, args=(raum_name,), daemon=True)
                http.rooms_dict[room_name]["thread_active"] = True
                abfrage_thread2.start()
              
                # hier soll thread 1 gestoppt werden, wenn er noch aktiv ist

                room_name_s=room_name.lower()
                r_s=room_name_s.replace(".", "_")
                print(r_s)
                try:
                    HA_req.change_temperature(f"input_number.heating_temperature_{r_s}",24)
                except :
                    print("mistake")
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
        except:
            print("aktuell keine sutnde")                   

        if room_data["state"] == 2 and room_name in belegung:
            if room_data["end_time"] and HA_req.get_current_time() > room_data["end_time"]:
                # Temperatur zurücksetzen
                print(f"Temperatur in {room_name} wird zurückgesetzt (Zeit ist abgelaufen).")
                # Hier kannst du z. B. einen Service aufrufen:
                try:
                    HA_req.change_temperature(f"input_number.heating_temperature_{r_s}",17)
                except :
                    print("mistake")
    print(lh.rooms_dict)
