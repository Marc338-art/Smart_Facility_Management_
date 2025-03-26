# main.py
#from http_requests.HA_req import get_current_lesson# Dein Modul, das die Funktion enthält

import http_requests # wenn man es so macht kann man keine methoden mit gleichem name in dem packet haben
def main():
     stunde=http_requests.get_current_lesson()

     http_requests.check_()

     print("Stunde: "+ str(stunde)) #Zugriff auf den ersten Teil der Liste 
    
if __name__ == "__main__":
    main()  # Start der Hauptanwendung
