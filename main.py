# main.py
#from http_requests.HA_req import *# Dein Modul, das die Funktion enthält

import http_requests # wenn man es so macht kann man keine methoden mit gleichem name in dem packet haben
def main():
    current_time = http_requests.change_temperature("input_number.heating_temperature")#akl
    

if __name__ == "__main__":
    main()  # Start der Hauptanwendung