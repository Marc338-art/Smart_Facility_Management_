# hier werden alle Funktionen von zustand 2 implementiert
from . import HA_req
from datetime import time
def update_act_lesson():
    if(HA_req.data_JSON["Belegung"]["A001"][0][HA_req.next_lesson]==1):  ## wenn alle Stunden belegt sind, geht er bis zur letzten und es wird erst nach der letzten in Zustand 1 gewechseltS
        HA_req.next_lesson+=1

    elif(HA_req.get_current_time()>HA_req.LESSON_HOURS[HA_req.next_lesson-1]["ende"]): # hier darf next_lesson nicht eine array index, sonder die wirkliche stunde
   
        HA_req.conditionFlag=1 # wenn die nächste Sutnde nicht belegt ist, soll in Zustand 1 gwechselt werden, sobald die Urhzeit zuende ist
        print(HA_req.conditionFlag)
        return
    
    print("act_lesoson"+str(HA_req.next_lesson))

def check_movement_Zustand_2():
    
    # es soll der Zustand des Bewegungssensors abgefragt werden. Es soll geprüft werden, ob er innerhalb von 30 Minuten mindestens einaml aktiv war.
    # sobald er einmal aktiv war soll die 30 Minuten erneut ablaufen und geprüft werden ob er in den 30 Minuten erneut triggert

    # man muss die Positiven flanken des Sensors prüfen, da er länger das Singal bewegung erkannt hält

    conditionFlag=1 # wenn nach 30 minuten keiner im raum ist, soll geprüft werden ob in 30 minuten die nächste stunde beginnt die belegt ist
    # man muss für den Fall aber als Parameter übergeben, dass es nicht in der aktuellen Stunde erneut geprüft wird 
    # (es muss also nur geprüft werden ob die aktuelle Stunde +30 min größer als das Ende der aktuellen Stunde ist)
    
    return
