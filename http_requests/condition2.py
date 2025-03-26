# hier werden alle Funktionen von zustand 2 implementiert
from .HA_req import*

def update_act_lesson():
    if(array_examplehours[next_lesson+1]==1):  ## wenn alle Stunden belegt ist, geht er bis zur letzten und es wird erst nach der letzten in Zustand 1 gewechseltS
        next_lesson+=1

    elif(get_current_time()>LESSON_HOURS[act_lesson]["ende"]):
        conditionFlag=1 # wenn die nächste Sutnde nicht belegt ist, soll in Zustand 1 gwechselt werden, sobald die Urhzeit zuende ist
        return


def check_movement_Zustand_2():
    
    # es soll der Zustand des Bewegungssensors abgefragt werden. Es soll geprüft werden, ob er innerhalb von 30 Minuten mindestens einaml aktiv war.
    # sobald er einmal aktiv war soll die 30 Minuten erneut ablaufen und geprüft werden ob er in den 30 Minuten erneut triggert

    # man muss die Positiven flanken des Sensors prüfen, da er länger das Singal bewegung erkannt hält

    conditionFlag=1 # wenn nach 30 minuten keiner im raum ist, soll geprüft werden ob in 30 minuten die nächste stunde beginnt die belegt ist
    # man muss für den Fall aber als Parameter übergeben, dass es nicht in der aktuellen Stunde erneut geprüft wird 
    # (es muss also nur geprüft werden ob die aktuelle Stunde +30 min größer als das Ende der aktuellen Stunde ist)
    
    return
