"""
Course: Data Structures & Algorithms
Core: Introduction to Data Structures
Task: 0
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


print(
    f"First record of texts, {texts[0][0]} texts {texts[0][1]} at time {texts[0][2]}")
print(
    f"Last record of calls, {calls[-1][0]} calls {calls[-1][1]} at time {calls[-1][2]}, lasting {calls[-1][3]} seconds"
)
