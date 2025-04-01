# hier ist der Code gespeichert, der im Zustant 1 benötigt wird
#from .HA_req import*
from . import HA_req



acttime=0


def get_timetable():
    #hier soll der http-Request zur Stundenplan API gemacht werden
    return None

def check_():
    
   
    # man kann die aktuelle Stunde als Zahlenwert in den Arrray der Räume packen (array[akt_stunde])
    current_lesson = HA_req.get_current_lesson()
    if( current_lesson==None):
        HA_req.change_temperature(HA_req.ROOMS["C009"]) # am besten die Temperatur nur bei veränderung ändern
        return
    else:
        if(HA_req.data["Belegung"][0][current_lesson-1]==1): # minus 1, da es keine Stunde 0 gibt
            HA_req.change_temperature(HA_req.ROOMS["C009"],21) #statt 21 eine constante übergeben
            

            HA_req.next_lesson=current_lesson-1 # da wir mit nextlesson wieder arrays addressieren wollen

            HA_req.conditionFlag=2 # soll gesetzt werden raum belegt ist und geheizt wird
            
            
        else:
            HA_req.change_temperature(HA_req.ROOMS["C009"])

            ## hier soll eine Flag gestzt werden, um in den Zustand 2 zu kommen.
    

def check_movement_Zustand1():

    # hier soll geprüft werden ob eine Bewegung  ist, obwohl de Raum micht belegt ist.
    # Es soll aber nicht bei einer Kurzen bewegung getriggetr werden, sondern  nur bei längeren
    # z.b 2 Positive Flanken des Bewegungssensors
    global acttime

    c_time=HA_req.t.time()
    move_act=HA_req.get_movement_sensor()
    movement_list=[]
    print(c_time)
    print(acttime)
    if(move_act is not None and acttime<=c_time-45 ): # überpfüfung soll für 10 Minuten durchgefüht werden, wenn es zweimal eine Bewegunng gibt, soll geheizt werden
        acttime=HA_req.t.time()
        movement_list.append(HA_req.get_movement_sensor())
        print("bewegung erkannt")
        return

    # es soll aber nur für 30 Minuten geheizt werden
    return