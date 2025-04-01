# main.py
#from http_requests.HA_req import get_current_lesson# Dein Modul, das die Funktion enthält
import sched
import time
import http_requests
from http_requests import HA_req




# Erstelle eine Instanz des schedulers
scheduler = sched.scheduler(time.time, time.sleep)



def main(): 
    
    print("Zustand"+str(HA_req.conditionFlag))
    # Hier definierst du deine Logik, die alle 20 Sekunden ausgeführt werden soll
    if(HA_req.conditionFlag == 1):  # Zustand 1
        
        #http_requests.check_()
        http_requests.check_movement_Zustand1()
        
        
    elif(HA_req.conditionFlag == 2):
        # Hier wird alles aus Zustand 2 aufgerufen
        #http_requests.update_act_lesson()
        http_requests.check_movement_Zustand1()

def schedule_task():
    # Plane die nächste Ausführung der main-Funktion in 20 Sekunden
    scheduler.enter(10, 1, schedule_task)  # Wiederhole alle 5 Sekunden
    main()  # Führe die main-Funktion aus

if __name__ == "__main__":
    # Starte den Scheduler und plane die erste Aufgabe
    schedule_task()
    # Starte die Ausführung des Schedulers
    scheduler.run()



## in die main muss ein try and except rein, da nicht jeder http ewquest funktioniert
