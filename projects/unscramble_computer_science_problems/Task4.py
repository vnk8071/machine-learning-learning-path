"""
Course: Data Structures & Algorithms
Core: Introduction to Data Structures
Task: 4
Code by: KhoiVN
Date: 29/01/2024
"""

import csv

TEXT_DATA = "texts.csv"
CALL_DATA = "calls.csv"

with open(TEXT_DATA, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    texts = list(reader)

with open(CALL_DATA, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    calls = list(reader)


possible_telemarketers = set()
avoid_telemarketers = set()

for call in calls:
    possible_telemarketers.add(call[0])
    avoid_telemarketers.add(call[1])

for text in texts:
    avoid_telemarketers.add(text[0])
    avoid_telemarketers.add(text[1])

telemarketers = possible_telemarketers.difference(avoid_telemarketers)
sorted_telemarketers = sorted(telemarketers)

print("These numbers could be telemarketers: ")
for telemarketer in sorted_telemarketers:
    print(telemarketer)
