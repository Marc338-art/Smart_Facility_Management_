# main.py
#from http_requests.HA_req import get_current_lesson# Dein Modul, das die Funktion enthält

import http_requests # wenn man es so macht kann man keine methoden mit gleichem name in dem packet haben
def main():
     
     if(http_requests.conditionFlag==1): #Zustand 1
        stunde=http_requests.get_current_lesson()

        http_requests.check_()
        http_requests.get_movement_sensor()
        print("Stunde: "+ str(stunde)) #Zugriff auf den ersten Teil der Liste 
     elif(http_requests.conditionFlag==2):
         # hier wir alles aus Zustand 2 aufgerufen
         print("zustand 2")



## je nach Zustand die methoder aufrufen
    
if __name__ == "__main__":
    main()  # Start der Hauptanwendung
