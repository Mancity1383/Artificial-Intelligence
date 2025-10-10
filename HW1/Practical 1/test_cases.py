"""
test_cases.py

Provides a list `cases` used by the template/solution scripts.
Each entry is a tuple: (courses, students, time_slots)

We include 8 cases:
- 3 easy
- 3 medium
- 2 hard
"""

cases = []

# -----------------
# Easy cases (3)
# -----------------
# Case E1: two courses conflict for same student
courses = ["Math", "Physics"]
students = {"s1": ["Math", "Physics"]}
time_slots = [1, 2]
cases.append((courses, students, time_slots))

# Case E2: small chain conflicts
courses = ["A", "B", "C"]
students = {"s1": ["A", "B"], "s2": ["B", "C"]}
time_slots = [1, 2]
cases.append((courses, students, time_slots))

# Case E3: three courses fully independent (no conflicts)
courses = ["X", "Y", "Z"]
students = {"s1": ["X"], "s2": ["Y"], "s3": ["Z"]}
time_slots = [1, 2]
cases.append((courses, students, time_slots))

# -----------------
# Medium cases (3)
# -----------------
# Case M1: moderate conflicts, needs 3 slots
courses = ["AI", "ML", "DB", "OS"]
students = {
    "s1": ["AI", "ML"],
    "s2": ["ML", "DB"],
    "s3": ["AI", "OS"]
}
time_slots = [1, 2, 3]
cases.append((courses, students, time_slots))

# Case M2: 5 courses, ring-like conflicts
courses = ["C1", "C2", "C3", "C4", "C5"]
students = {
    "s1": ["C1", "C2"],
    "s2": ["C2", "C3"],
    "s3": ["C3", "C4"],
    "s4": ["C4", "C5"]
}
time_slots = [1, 2, 3]
cases.append((courses, students, time_slots))

# Case M3: denser conflicts
courses = ["P", "Q", "R", "S"]
students = {
    "a": ["P", "Q"], "b": ["Q", "R"], "c": ["R", "S"], "d": ["P", "S"], "e": ["P", "R"]
}
time_slots = [1, 2, 3]
cases.append((courses, students, time_slots))

# -----------------
# Hard cases (2)
# -----------------
# Case H1: 6 courses, tight slots (3 slots)
courses = ["M1", "M2", "M3", "M4", "M5", "M6"]
students = {
    "s1": ["M1","M2"], "s2": ["M2","M3"], "s3": ["M3","M4"],
    "s4": ["M4","M5"], "s5": ["M5","M6"], "s6": ["M1","M6"]
}
time_slots = [1, 2, 3]
cases.append((courses, students, time_slots))

# Case H2: 8 courses, 4 slots, fairly dense conflict graph
courses = ["CS1","CS2","CS3","CS4","CS5","CS6","CS7","CS8"]
students = {
    "u1": ["CS1","CS2"], "u2": ["CS2","CS3"], "u3": ["CS3","CS4"],
    "u4": ["CS4","CS5"], "u5": ["CS5","CS6"], "u6": ["CS6","CS7"],
    "u7": ["CS7","CS8"], "u8": ["CS8","CS1"], "u9": ["CS1","CS3"], "u10": ["CS2","CS4"]
}
time_slots = [1,2,3,4]
cases.append((courses, students, time_slots))
