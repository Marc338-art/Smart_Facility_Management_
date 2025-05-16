from datetime import time


LESSON_HOURS = [  ## der Stundenplan soll als sperate .py gespeichert werden um als Impirt auf i
    {"stunde": 1, "start": time(7, 30), "ende": time(8, 15)},
    {"stunde": 2, "start": time(8, 15), "ende": time(9, 0)},
    {"stunde": 3, "start": time(9, 20), "ende": time(10, 5)},
    {"stunde": 4, "start": time(10, 5), "ende": time(10, 50)},
    {"stunde": 5, "start": time(11, 10), "ende": time(11, 55)},
    {"stunde": 6, "start": time(11, 55), "ende": time(12, 40)},
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


## hier sollen alle Räume und Heizvariablen ergänzt werden   (Wahrscheinlich nicht mehr nötig)
ROOMS1 ={
    'C005': "input_number.heating_temperature_c005",
    'C009': "input_number.heating_temperature_c009"

}

rooms = [
    "A023", "Room_02", "Room_03", "A024", "A028", "A025", "Room_07", "Room_08",
    "Room_09", "Room_10", "Room_11", "Room_12", "Room_13", "Room_14", "Room_15",
    "Room_16", "Room_17", "Room_18", "Room_19", "Room_20", "Room_21", "Room_22",
    "Room_23", "Room_24", "Room_25", "Room_26", "Room_27", "Room_28", "Room_29",
    "Room_30", "Room_31", "Room_32", "Room_33", "Room_34", "Room_35", "Room_36",
    "Room_37", "Room_38", "Room_39", "Room_40"
]
 
default_end_time = time(20, 30) 
rooms_dict = {name: {"state": 1, "end_time": default_end_time} for name in rooms}
rooms = [{"name": name, "state": 1, "end_time": default_end_time} for name in rooms]

