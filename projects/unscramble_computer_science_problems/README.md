# Investigating Texts and Calls

## Project Overview

In this project, you will complete five tasks based on a fabricated set of calls and texts exchanged during September 2016. You will use Python to analyze and answer questions about the texts and calls contained in the dataset. Lastly, you will perform run time analysis of your solution and determine its efficiency.

## About the data

The text and call data are provided in csv files.
The text data `(text.csv)` has the following columns: sending telephone number (string), receiving telephone number (string), timestamp of text message (string).
The call data `(call.csv)` has the following columns: calling telephone number (string), receiving telephone number (string), start timestamp of telephone call (string), duration of telephone call in seconds (string)

All telephone numbers are 10 or 11 numerical digits long. Each telephone number starts with a code indicating the location and/or type of the telephone number. There are three different kinds of telephone numbers, each with a different format:

- Fixed lines start with an area code enclosed in brackets. The area codes vary in length but always begin with 0. Example: "(022)40840621".
- Mobile numbers have no parentheses, but have a space in the middle of the number to help readability. The mobile code of a mobile number is its first four digits and they always start with 7, 8 or 9. Example: "93412 66159".
- Telemarketers' numbers have no parentheses or space, but start with the code 140. Example: "1402316533".

## Task 0

What is the first record of texts and what is the last record of calls?

>Print messages:
"First record of texts, <incoming number> texts <answering number> at time <time>"
"Last record of calls, <incoming number> calls <answering number> at time <time>, lasting <during> seconds"

```python
python Task0.py
```

Output:

```python
First record of texts, 97424 22395 texts 90365 06212 at time 01-09-2016 06:03:22
Last record of calls, 98447 62998 calls (080)46304537 at time 30-09-2016 23:57:15, lasting 2151 seconds
```

## Task 1

How many different telephone numbers are there in the records?

>Print a message:
"There are <count> different telephone numbers in the records."

```python
python Task1.py
```

Output:

```python
There are 570 different telephone numbers in the records.
```

## Task 2

Which telephone number spent the longest time on the phone during the period? Don't forget that time spent answering a call is also time spent on the phone.

>Print a message:
"<telephone number> spent the longest time, <total time> seconds, on the phone during September 2016.".

```python
python Task2.py
```

Output:

```python
(080)33251027 spent the longest time, 90456 seconds, on the phone during September 2016.
```

## Task 3

(080) is the area code for fixed line telephones in Bangalore. Fixed line numbers include parentheses, so Bangalore numbers have the form (080)xxxxxxx.

Part A: Find all of the area codes and mobile prefixes called by people in Bangalore. In other words, the calls were initiated by "(080)" area code to the following area codes and mobile prefixes:

- Fixed lines start with an area code enclosed in brackets. The area codes vary in length but always begin with 0.
- Mobile numbers have no parentheses, but have a space in the middle of the number to help readability. The prefix of a mobile number is its first four digits, and they always start with 7, 8 or 9.
- Telemarketers' numbers have no parentheses or space, but they start with the area code 140.

>Print the answer as part of a message:
"The numbers called by people in Bangalore have codes:"
 <list of codes>
The list of codes should be print out one per line in lexicographic order with no duplicates.

Part B: What percentage of calls from fixed lines in Bangalore are made to fixed lines also in Bangalore? In other words, of all the calls made from a number starting with "(080)", what percentage of these calls were made to a number also starting with "(080)"?

>Print the answer as a part of a message::
"<percentage> percent of calls from fixed lines in Bangalore are calls
to other fixed lines in Bangalore."
The percentage should have 2 decimal digits

```python
Part A:
The numbers called by people in Bangalore have codes:
(022)
(040)
(04344)
(044)
(04546)
(0471)
(080)
(0821)
7406
7795
7813
7829
8151
8152
8301
8431
8714
9008
9019
9035
9036
9241
9242
9341
9342
9343
9400
9448
9449
9526
9656
9738
9740
9741
9742
9844
9845
9900
9961
----------------------------------------
Part B:
24.81 percent of calls from fixed lines in Bangalore are calls to other fixed lines in Bangalore.
```

## Task 4

The telephone company want to identify numbers that might be doing telephone marketing. Create a set of possible telemarketers: these are numbers that make outgoing calls but never send texts, receive texts or receive incoming calls.

>Print a message:
"These numbers could be telemarketers: "
<list of numbers>
The list of numbers should be print out one per line in lexicographic order with no duplicates.

```python
python Task4.py
```

Output:

```python
These numbers could be telemarketers:
(022)37572285
(022)65548497
(022)68535788
(022)69042431
(040)30429041
(044)22020822
(0471)2171438
(0471)6579079
(080)20383942
(080)25820765
(080)31606520
(080)40362016
(080)60463379
(080)60998034
(080)62963633
(080)64015211
(080)69887826
(0821)3257740
1400481538
1401747654
1402316533
1403072432
1403579926
1404073047
1404368883
1404787681
1407539117
1408371942
1408409918
1408672243
1409421631
1409668775
1409994233
74064 66270
78291 94593
87144 55014
90351 90193
92414 69419
94495 03761
97404 30456
97407 84573
97442 45192
99617 25274
```
