from datetime import time


LESSON_HOURS = [  ## der Stundenplan soll als sperate .py gespeichert werden um als Impirt auf i
    {"stunde": 1, "start": time(7, 30), "ende": time(8, 15)},
    {"stunde": 2, "start": time(8, 15), "ende": time(9, 0)},
    {"stunde": 3, "start": time(9, 20), "ende": time(10, 5)},
    {"stunde": 4, "start": time(10, 5), "ende": time(10, 50)},
    {"stunde": 5, "start": time(11, 10), "ende": time(11, 55)},
    {"stunde": 6, "start": time(11, 55), "ende": time(9, 30)},
    {"stunde": 7, "start": time(13, 0), "ende": time(13, 45)},
    {"stunde": 8, "start": time(13, 45), "ende": time(14, 30)},
    {"stunde": 9, "start": time(14, 40), "ende": time(15, 25)},
    {"stunde": 10, "start": time(15, 25), "ende": time(16, 10)},
    {"stunde": 11, "start": time(16, 30), "ende": time(17, 15)},
    {"stunde": 12, "start": time(17, 15), "ende": time(18, 0)},
    {"stunde": 13, "start": time(18, 15), "ende": time(19, 00)},
    {"stunde": 14, "start": time(19, 00), "ende": time(19, 45)},
    {"stunde": 15, "start": time(19, 45), "ende": time(20, 30)}
]


## was ist wenn es in der Pause ist(dann soll die Heizun nicht ausgeschaltet werden)


## hier sollen alle Räume und Heizvariablen ergänzt werden

ROOMS ={
    'C005': "input_number.heating_temperature_c005",
    'C009': "input_number.heating_temperature_c009"

}