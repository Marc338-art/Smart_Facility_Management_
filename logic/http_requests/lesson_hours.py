from datetime import time

# -----------------------------------------------------------------------------------
# Stundenplan: Start- und Endzeiten der Unterrichtsstunden
# -----------------------------------------------------------------------------------

LESSON_HOURS = [
    {"stunde": 1,  "start": time(7, 30),  "ende": time(8, 15)},
    {"stunde": 2,  "start": time(8, 15),  "ende": time(9, 0)},
    {"stunde": 3,  "start": time(9, 20),  "ende": time(10, 5)},
    {"stunde": 4,  "start": time(10, 5),  "ende": time(10, 50)},
    {"stunde": 5,  "start": time(11, 10), "ende": time(11, 55)},
    {"stunde": 6,  "start": time(11, 55), "ende": time(12, 40)},
    {"stunde": 7,  "start": time(13, 0),  "ende": time(13, 45)},
    {"stunde": 8,  "start": time(13, 45), "ende": time(14, 30)},
    {"stunde": 9,  "start": time(14, 40), "ende": time(15, 25)},
    {"stunde": 10, "start": time(15, 25), "ende": time(16, 10)},
    {"stunde": 11, "start": time(16, 30), "ende": time(17, 15)},
    {"stunde": 12, "start": time(17, 15), "ende": time(18, 0)},
    {"stunde": 13, "start": time(18, 15), "ende": time(19, 0)},
    {"stunde": 14, "start": time(19, 0),  "ende": time(19, 45)},
    {"stunde": 15, "start": time(19, 45), "ende": time(20, 30)},
]

# -----------------------------------------------------------------------------------
# Raumliste (für das Heizungs- und Präsenzmanagement)
# -----------------------------------------------------------------------------------

rooms = [
    "C001", "C002", "C003.1", "C003.3", "C004", "C005", "C011", "C016", "C017",
    "C101", "C104", "C106", "C109.1", "C110", "C111", "C112", "C115", "C116",
    "C201", "C202", "C205", "C208", "C209", "C212", "C219", "C220"
]

# -----------------------------------------------------------------------------------
# Raumstatus (initialisiert auf "inaktiv" mit keinem laufenden Thread)
# -----------------------------------------------------------------------------------

rooms_dict = {
    name: {
        "state": 1,             # 1 = inaktiv, 2 = aktiv
        "thread_active": False  # Gibt an, ob ein Überwachungsthread läuft
    }
    for name in rooms
}


