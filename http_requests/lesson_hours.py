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

rooms = [
    {"name": "Room_01", "state": 1},
    {"name": "Room_02", "state": 2},
    {"name": "Room_03", "state": 1},
    {"name": "Room_04", "state": 2},
    {"name": "Room_05", "state": 1},
    {"name": "Room_06", "state": 2},
    {"name": "Room_07", "state": 1},
    {"name": "Room_08", "state": 2},
    {"name": "Room_09", "state": 1},
    {"name": "Room_10", "state": 2},
    {"name": "Room_11", "state": 1},
    {"name": "Room_12", "state": 2},
    {"name": "Room_13", "state": 1},
    {"name": "Room_14", "state": 2},
    {"name": "Room_15", "state": 1},
    {"name": "Room_16", "state": 2},
    {"name": "Room_17", "state": 1},
    {"name": "Room_18", "state": 2},
    {"name": "Room_19", "state": 1},
    {"name": "Room_20", "state": 2},
    {"name": "Room_21", "state": 1},
    {"name": "Room_22", "state": 2},
    {"name": "Room_23", "state": 1},
    {"name": "Room_24", "state": 2},
    {"name": "Room_25", "state": 1},
    {"name": "Room_26", "state": 2},
    {"name": "Room_27", "state": 1},
    {"name": "Room_28", "state": 2},
    {"name": "Room_29", "state": 1},
    {"name": "Room_30", "state": 2},
    {"name": "Room_31", "state": 1},
    {"name": "Room_32", "state": 2},
    {"name": "Room_33", "state": 1},
    {"name": "Room_34", "state": 2},
    {"name": "Room_35", "state": 1},
    {"name": "Room_36", "state": 2},
    {"name": "Room_37", "state": 1},
    {"name": "Room_38", "state": 2},
    {"name": "Room_39", "state": 1},
    {"name": "Room_40", "state": 2},
]
