"""
Course: Data Structures & Algorithms
Core: Introduction to Data Structures
Task: 1
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


count_unique_telephone_numbers = set()
for text, call in zip(texts, calls):
    count_unique_telephone_numbers.add(text[0])
    count_unique_telephone_numbers.add(text[1])
    count_unique_telephone_numbers.add(call[0])
    count_unique_telephone_numbers.add(call[1])

print(
    f"There are {len(count_unique_telephone_numbers)} different telephone numbers in the records."
)
