"""
Course: Data Structures & Algorithms
Core: Introduction to Data Structures
Task: 3
Code by: KhoiVN
Date: 29/01/2024
"""

import csv

CALL_DATA = "calls.csv"

with open(CALL_DATA, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    calls = list(reader)


bangalore_number_calles = set()

for call in calls:
    if call[0].startswith("(080)"):
        if call[1].startswith("("):
            bangalore_number_calles.add(call[1][: call[1].find(")") + 1])
        elif call[1].startswith("140"):
            bangalore_number_calles.add(call[1][:3])
        elif (
            call[1].startswith("7")
            or call[1].startswith("8")
            or call[1].startswith("9")
        ):
            bangalore_number_calles.add(call[1][:4])

print("Part A:")
print("The numbers called by people in Bangalore have codes:")

sorted_bangalore_number_calles = sorted(bangalore_number_calles)
for number_call in sorted_bangalore_number_calles:
    print(number_call)

print("----------------------------------------")
print("Part B:")

count_calling = 0
count_receiving = 0

for call in calls:
    if call[0].startswith("(080)"):
        count_calling += 1
        if call[1].startswith("(080)"):
            count_receiving += 1

print(
    f"{round(count_receiving/count_calling*100, 2)} percent of calls from fixed lines in Bangalore are calls to other fixed lines in Bangalore."
)
