# hier ist der Code gespeichert, der im Zustant 1 benötigt wird
from .HA_req import*
def get_timetable():
    #hier soll der http-Request zur Stundenplan API gemacht werden
    return None

def check_():
    

    # man kann die aktuelle Stunde als Zahlenwert in den Arrray der Räume packen (array[akt_stunde])
    current_lesson = get_current_lesson()
    if( current_lesson==None):
        change_temperature(ROOMS["C009"]) # erstelle ein array mit allen räumen und der heating temperature für jeden Raumn
        return
    else:
        if(array_examplehours[get_current_lesson()]==1):
            change_temperature(ROOMS["C009"],21) #statt 21 eine constante übergeben
            conditionFlag=2 # soll gesetzt werden raum belegt ist und geheizt wird
            act_lesson=current_lesson
        else:
            change_temperature(ROOMS["C009"])

            ## hier soll eine Flag gestzt werden, um in den Zustand 2 zu kommen.
    

def check_movement_Zustand1():

    # hier soll geprüft werden ob eine Bewegung  ist, obwohl de Raum micht belegt ist.
    # Es soll aber nicht bei einer Kurzen bewegung getriggetr werden, sondern  nur bei längeren
    # z.b 2 Positive Flanken des Bewegungssensors

    movement_list=[]

    if(get_movement_sensor()!=None): # überpfüfung soll für 10 Minuten durchgefüht werden, wenn es zweimal eine Bewegunng gibt, soll geheizt werden
        return

    # es soll aber nur für 30 Minuten geheizt werden
    return