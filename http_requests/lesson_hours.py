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

rooms = [
    "C001","C002","C003.1", "C003.2", "C003.3", "C003.4", "C003.5", "C004", "C005", "C006.1",
    "C006.2", "C006.3", "C007", "C008", "C009", "C011", "C012",
    "C013", "C014", "C015", "C016", "C017", "C018", "C101",
    "C102", "C103", "C104", "C105", "C106", "C107", "C108","C109.1","C109.2","C110","C111",
    "C112", "C113", "C114", "C115", "C116", "C117", "C117","C201","C202","C203","C204","C205",
    "C206", "C207", "C208", "C209","C210","C211","C212","C213","C214","C215","C216","C217",
    "C218","C219","C220","C221"
]
 
default_end_time = time(20, 30) 
rooms_dict = {
    name: {
        "state": 1,
        "end_time": default_end_time,
        "thread_active": False  # Neue Variable für Thread-Zustand
    }
    for name in rooms
}
rooms = [{"name": name, "state": 1, "end_time": default_end_time} for name in rooms]

