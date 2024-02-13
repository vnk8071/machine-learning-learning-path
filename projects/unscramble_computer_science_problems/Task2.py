"""
Course: Data Structures & Algorithms
Core: Introduction to Data Structures
Task: 2
Code by: KhoiVN
Date: 29/01/2024
"""

import csv
from collections import defaultdict


CALL_DATA = "calls.csv"

with open(CALL_DATA, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    calls = list(reader)


total_duration_calls = defaultdict(int)
for call in calls:
    total_duration_calls[call[0]] += int(call[3])
    total_duration_calls[call[1]] += int(call[3])

max_duration_call = sorted(
    total_duration_calls.items(), key=lambda x: x[1], reverse=True
)[0]

print(
    f"{max_duration_call[0]} spent the longest time, {max_duration_call[1]} seconds, on the phone during September 2016."
)
