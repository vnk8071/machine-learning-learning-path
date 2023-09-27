# Explore Close Approaches of Near-Earth Objects

In this project, you'll use Python - and the skills we've developed throughout this course - to search for and explore close approaches of near-Earth objects (NEOs), using data from NASA/JPL's Center for Near Earth Object Studies.

## Overview

At a high-level, you'll create Python code that implements a command-line tool to inspect and query a dataset of NEOs and their close approaches to Earth.

Concretely, you'll have to read data from both a CSV file and a JSON file, convert that data into structured Python objects, perform filtering operations on the data, limit the size of the result set, and write the results to a file in a structured format, such as CSV or JSON.

When complete, you'll be able to inspect the properties of the near-Earth objects in the data set and query the data set of close approaches to Earth using any combination of the following filters:

- Occurs on a given date.
- Occurs on or after a given start date.
- Occurs on or before a given end date.
- Approaches Earth at a distance of at least (or at most) X astronomical units.
- Approaches Earth at a relative velocity of at least (or at most) Y kilometers per second.
- Has a diameter that is at least as large as (or at least as small as) Z kilometers.
- Is marked by NASA as potentially hazardous (or not).

## Getting Started
### Prerequisites
Using Python 3.8 or later, install the required packages listed in `requirements.txt` using `pip` or your favorite package manager (e.g. `conda`).

### Installing
pip install -r requirements.txt

### Lint and Format
```bash
flake8 .
autopep8 --in-place --aggressive --aggressive *.py
```

## Understanding the Near-Earth Object Close Approach Datasets

This project contains two important data sets, and our first step will be to explore and understand the data containing within these structured files.

One dataset (`neos.csv`) contains information about semantic, physical, orbital, and model parameters for certain small bodies (asteroids and comets, mostly) in our solar system. The other dataset (`cad.json`) contains information about NEO close approaches - moments in time when the orbit of an astronomical body brings it close to Earth. NASA helpfully provides a [glossary](https://cneos.jpl.nasa.gov/glossary/) to define any unfamiliar terms you might encounter.

Importantly, these datasets come directly from NASA - we haven't dressed them up for you at all.

## Task 1
```python
python models.py
```

Result
```
2023-09-27 21:53:07,583 - __main__ - INFO - Running models.py directly
2023-09-27 21:53:07,583 - __main__ - INFO - Creating NearEarthObject
2023-09-27 21:53:07,583 - __main__ - INFO - 2020 FK
2023-09-27 21:53:07,583 - __main__ - INFO - One REALLY BIG fake asteroid
2023-09-27 21:53:07,583 - __main__ - INFO - 12.345
2023-09-27 21:53:07,583 - __main__ - INFO - True
2023-09-27 21:53:07,583 - __main__ - INFO - Creating CloseApproach
2023-09-27 21:53:07,587 - __main__ - INFO - 2020-01-01 12:00
2023-09-27 21:53:07,587 - __main__ - INFO - 0.25
2023-09-27 21:53:07,587 - __main__ - INFO - 56.78
2023-09-27 21:53:07,587 - __main__ - INFO - At 2020-01-01 12:00, '' approaches Earth at a distance of 0.25 au and a velocity of 56.78 km/s.
```

## Task 2
### 2.1 Extract
```python
python extract.py
```

Result
```
2023-09-27 22:42:36,626 - __main__ - INFO - Running load_neos with data/neos.csv file
2023-09-27 22:42:36,965 - __main__ - INFO - First NEO: A NearEarthObject is 433 Eros, which is 16.840 km in diameter and is not potentially hazardous.
2023-09-27 22:42:36,965 - __main__ - INFO - Last NEO: A NearEarthObject is 2020 P4-C , which is nan km in diameter and is not potentially hazardous.
2023-09-27 22:42:36,965 - __main__ - INFO - load_neos passed
2023-09-27 22:42:36,965 - __main__ - INFO - Running load_approaches with data/cad.json file
2023-09-27 22:42:43,497 - models - INFO - Running __str__
2023-09-27 22:42:43,497 - models - INFO - Running time_str
2023-09-27 22:42:43,497 - models - INFO - Running fullname
2023-09-27 22:42:43,497 - __main__ - INFO - First approach: At 1900-01-01 00:11, '170903' approaches Earth at a distance of 0.09 au and a velocity of 16.75 km/s.
2023-09-27 22:42:43,497 - models - INFO - Running __str__
2023-09-27 22:42:43,498 - models - INFO - Running time_str
2023-09-27 22:42:43,498 - models - INFO - Running fullname
2023-09-27 22:42:43,498 - __main__ - INFO - Last approach: At 2099-12-31 20:51, '2010 XB24' approaches Earth at a distance of 0.13 au and a velocity of 16.68 km/s.
2023-09-27 22:42:43,498 - __main__ - INFO - load_approaches passed
```

### 2.2 Database
```python
# Map the designation of the NEO to the designation of the approach
self._neos_index = {neo.designation: index for index, neo in enumerate(self._neos)}
self._cas_index = {}
for ca in self._approaches:
    if ca._designation in self._cas_index:
        self._cas_index[ca._designation].append(ca)
    else:
        self._cas_index[ca._designation] = [ca]

for neo in self._neos:
    if neo.designation in self._cas_index:
        neo.approaches = self._cas_index[neo.designation]

for ca in self._approaches:
    if ca._designation in self._neos_index:
        ca.neo = self._neos[self._neos_index[ca._designation]]
```

### Testing
```python
python -m unittest tests.test_extract tests.test_database
```

Result
```
................2023-09-27 23:03:30,367 - database - INFO - Searching for NEO with designation: 1865
2023-09-27 23:03:30,367 - database - INFO - Searching for NEO with designation: 2101
2023-09-27 23:03:30,367 - database - INFO - Searching for NEO with designation: 2102
.2023-09-27 23:03:30,367 - database - INFO - Searching for NEO with designation: not-real-designation
.2023-09-27 23:03:30,368 - database - INFO - Searching for NEO with designation: 2020 BS
2023-09-27 23:03:30,368 - database - INFO - Searching for NEO with designation: 2020 PY1
.2023-09-27 23:03:30,368 - database - INFO - Searching for NEO with name: Lemmon
2023-09-27 23:03:30,369 - database - INFO - Searching for NEO with name: Jormungandr
.2023-09-27 23:03:30,369 - database - INFO - Searching for NEO with name: not-real-name
.
----------------------------------------------------------------------
Ran 21 tests in 1.826s

OK
```

## Task 3
### 3.1 Query
```bash
python main.py query --start-date 2020-01-01 --end-date 2020-12-31
```

Result
```
2023-09-28 00:24:21,368 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-01-01), DateFilter(op=operator.le, value=2020-12-31)]
At 2020-01-01 00:54, 2020 AY1 approaches Earth at a distance of 0.02 au and a velocity of 5.62 km/s.
At 2020-01-01 02:06, 2019 YK approaches Earth at a distance of 0.04 au and a velocity of 7.36 km/s.
At 2020-01-01 03:31, 2013 EC20 approaches Earth at a distance of 0.16 au and a velocity of 2.79 km/s.
At 2020-01-01 07:18, 2020 AM1 approaches Earth at a distance of 0.16 au and a velocity of 4.15 km/s.
At 2020-01-01 08:44, 2016 EF195 approaches Earth at a distance of 0.28 au and a velocity of 17.55 km/s.
At 2020-01-01 11:13, 2020 AP3 approaches Earth at a distance of 0.02 au and a velocity of 5.19 km/s.
At 2020-01-01 14:36, 2011 YE40 approaches Earth at a distance of 0.06 au and a velocity of 12.79 km/s.
At 2020-01-01 14:55, 2019 WE5 approaches Earth at a distance of 0.13 au and a velocity of 5.00 km/s.
At 2020-01-01 15:16, 2020 AE2 approaches Earth at a distance of 0.24 au and a velocity of 13.30 km/s.
At 2020-01-01 21:01, 2020 JU approaches Earth at a distance of 0.13 au and a velocity of 6.65 km/s.
```

### 3.2 Limit
```bash
python main.py query --start-date 2020-01-01 --end-date 2020-12-31 --hazardous --min-diameter 0.25 --max-distance 0.1 --limit 5
```

Result
```
2023-09-28 00:26:39,903 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-01-01), DateFilter(op=operator.le, value=2020-12-31), DistanceFilter(op=operator.le, value=0.1), DiameterFilter(op=operator.ge, value=0.25), HazardousFilter(op=operator.eq, value=True)]
At 2020-04-29 09:56, 52768 approaches Earth at a distance of 0.04 au and a velocity of 8.70 km/s.
At 2020-06-06 03:20, 163348 approaches Earth at a distance of 0.03 au and a velocity of 11.15 km/s.
At 2020-07-14 11:12, 480936 approaches Earth at a distance of 0.09 au and a velocity of 9.82 km/s.
At 2020-07-23 23:09, 8014 approaches Earth at a distance of 0.05 au and a velocity of 7.64 km/s.
At 2020-11-29 05:08, 153201 approaches Earth at a distance of 0.03 au and a velocity of 25.07 km/s.
```

### Testing
```python
python -m unittest tests.test_query tests.test_limit
```

Result
```
2023-09-27 23:54:34,248 - database - INFO - Querying for close approaches with filters: []
.2023-09-27 23:54:34,250 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-04-01)]
.2023-09-27 23:54:34,255 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.le, value=2020-06-30)]
.2023-09-27 23:54:34,259 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-03-31)]
.2023-09-27 23:54:34,265 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-03-31), DistanceFilter(op=operator.ge, value=0.1), DistanceFilter(op=operator.le, value=0.4), VelocityFilter(op=operator.ge, value=10), VelocityFilter(op=operator.le, value=20)]
.2023-09-27 23:54:34,280 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-03-31), DistanceFilter(op=operator.ge, value=0.1), DistanceFilter(op=operator.le, value=0.4), VelocityFilter(op=operator.le, value=20)]
.2023-09-27 23:54:34,293 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-03-31), DistanceFilter(op=operator.ge, value=0.1), DistanceFilter(op=operator.le, value=0.4)]
.2023-09-27 23:54:34,304 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-05-31), DistanceFilter(op=operator.ge, value=0.05), DistanceFilter(op=operator.le, value=0.5), VelocityFilter(op=operator.ge, value=5), VelocityFilter(op=operator.le, value=25), DiameterFilter(op=operator.ge, value=0.5), DiameterFilter(op=operator.le, value=1.5), HazardousFilter(op=operator.eq, value=False)]
.2023-09-27 23:54:34,326 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-05-31), DistanceFilter(op=operator.ge, value=0.05), DistanceFilter(op=operator.le, value=0.5), VelocityFilter(op=operator.ge, value=5), VelocityFilter(op=operator.le, value=25), DiameterFilter(op=operator.ge, value=0.5), DiameterFilter(op=operator.le, value=1.5), HazardousFilter(op=operator.eq, value=True)]
.2023-09-27 23:54:34,347 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-05-31), DistanceFilter(op=operator.ge, value=0.05), DistanceFilter(op=operator.le, value=0.5), VelocityFilter(op=operator.ge, value=5), VelocityFilter(op=operator.le, value=25), DiameterFilter(op=operator.le, value=1.5)]
.2023-09-27 23:54:34,364 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-05-31), DistanceFilter(op=operator.ge, value=0.05), DistanceFilter(op=operator.le, value=0.5), VelocityFilter(op=operator.ge, value=5), VelocityFilter(op=operator.le, value=25), DiameterFilter(op=operator.ge, value=0.5), DiameterFilter(op=operator.le, value=1.5)]
.2023-09-27 23:54:34,384 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.eq, value=2020-03-02)]
.2023-09-27 23:54:34,388 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.eq, value=2020-03-02), DistanceFilter(op=operator.le, value=0.4)]
.2023-09-27 23:54:34,395 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.eq, value=2020-03-02), DistanceFilter(op=operator.ge, value=0.1)]
.2023-09-27 23:54:34,401 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.eq, value=2020-03-02), DateFilter(op=operator.ge, value=2020-02-01), DateFilter(op=operator.le, value=2020-04-01)]
.2023-09-27 23:54:34,409 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-10-01), DateFilter(op=operator.le, value=2020-04-01)]
.2023-09-27 23:54:34,416 - database - INFO - Querying for close approaches with filters: [HazardousFilter(op=operator.eq, value=True)]
.2023-09-27 23:54:34,421 - database - INFO - Querying for close approaches with filters: [DiameterFilter(op=operator.le, value=1.5)]
.2023-09-27 23:54:34,426 - database - INFO - Querying for close approaches with filters: [DiameterFilter(op=operator.ge, value=0.5), DiameterFilter(op=operator.le, value=1.5)]
.2023-09-27 23:54:34,433 - database - INFO - Querying for close approaches with filters: [DiameterFilter(op=operator.ge, value=1.5), DiameterFilter(op=operator.le, value=0.5)]
.2023-09-27 23:54:34,440 - database - INFO - Querying for close approaches with filters: [DistanceFilter(op=operator.le, value=0.4)]
.2023-09-27 23:54:34,444 - database - INFO - Querying for close approaches with filters: [DistanceFilter(op=operator.ge, value=0.1), DistanceFilter(op=operator.le, value=0.4)]
.2023-09-27 23:54:34,450 - database - INFO - Querying for close approaches with filters: [DistanceFilter(op=operator.ge, value=0.4), DistanceFilter(op=operator.le, value=0.1)]
.2023-09-27 23:54:34,457 - database - INFO - Querying for close approaches with filters: [VelocityFilter(op=operator.le, value=20)]
.2023-09-27 23:54:34,461 - database - INFO - Querying for close approaches with filters: [VelocityFilter(op=operator.ge, value=10), VelocityFilter(op=operator.le, value=20)]
.2023-09-27 23:54:34,467 - database - INFO - Querying for close approaches with filters: [VelocityFilter(op=operator.ge, value=20), VelocityFilter(op=operator.le, value=10)]
.2023-09-27 23:54:34,474 - database - INFO - Querying for close approaches with filters: [DiameterFilter(op=operator.ge, value=0.5)]
.2023-09-27 23:54:34,478 - database - INFO - Querying for close approaches with filters: [DistanceFilter(op=operator.ge, value=0.1)]
.2023-09-27 23:54:34,483 - database - INFO - Querying for close approaches with filters: [VelocityFilter(op=operator.ge, value=10)]
.2023-09-27 23:54:34,488 - database - INFO - Querying for close approaches with filters: [HazardousFilter(op=operator.eq, value=False)]
........
----------------------------------------------------------------------
Ran 37 tests in 2.089s

OK
```

## Task 4
### Testing
```python
python -m unittest
```

Result
```
........2023-09-28 00:07:03,318 - database - INFO - Searching for NEO with designation: 1865
2023-09-28 00:07:03,324 - database - INFO - Searching for NEO with designation: 2101
2023-09-28 00:07:03,324 - database - INFO - Searching for NEO with designation: 2102
.2023-09-28 00:07:03,324 - database - INFO - Searching for NEO with designation: not-real-designation
.2023-09-28 00:07:03,325 - database - INFO - Searching for NEO with designation: 2020 BS
2023-09-28 00:07:03,326 - database - INFO - Searching for NEO with designation: 2020 PY1
.2023-09-28 00:07:03,326 - database - INFO - Searching for NEO with name: Lemmon
2023-09-28 00:07:03,327 - database - INFO - Searching for NEO with name: Jormungandr
.2023-09-28 00:07:03,327 - database - INFO - Searching for NEO with name: not-real-name
.....................2023-09-28 00:07:05,131 - database - INFO - Querying for close approaches with filters: []
.2023-09-28 00:07:05,133 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-04-01)]
.2023-09-28 00:07:05,137 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.le, value=2020-06-30)]
.2023-09-28 00:07:05,141 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-03-31)]
.2023-09-28 00:07:05,153 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-03-31), DistanceFilter(op=operator.ge, value=0.1), DistanceFilter(op=operator.le, value=0.4), VelocityFilter(op=operator.ge, value=10), VelocityFilter(op=operator.le, value=20)]
.2023-09-28 00:07:05,167 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-03-31), DistanceFilter(op=operator.ge, value=0.1), DistanceFilter(op=operator.le, value=0.4), VelocityFilter(op=operator.le, value=20)]
.2023-09-28 00:07:05,179 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-03-31), DistanceFilter(op=operator.ge, value=0.1), DistanceFilter(op=operator.le, value=0.4)]
.2023-09-28 00:07:05,190 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-05-31), DistanceFilter(op=operator.ge, value=0.05), DistanceFilter(op=operator.le, value=0.5), VelocityFilter(op=operator.ge, value=5), VelocityFilter(op=operator.le, value=25), DiameterFilter(op=operator.ge, value=0.5), DiameterFilter(op=operator.le, value=1.5), HazardousFilter(op=operator.eq, value=False)]
.2023-09-28 00:07:05,211 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-05-31), DistanceFilter(op=operator.ge, value=0.05), DistanceFilter(op=operator.le, value=0.5), VelocityFilter(op=operator.ge, value=5), VelocityFilter(op=operator.le, value=25), DiameterFilter(op=operator.ge, value=0.5), DiameterFilter(op=operator.le, value=1.5), HazardousFilter(op=operator.eq, value=True)]
.2023-09-28 00:07:05,231 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-05-31), DistanceFilter(op=operator.ge, value=0.05), DistanceFilter(op=operator.le, value=0.5), VelocityFilter(op=operator.ge, value=5), VelocityFilter(op=operator.le, value=25), DiameterFilter(op=operator.le, value=1.5)]
.2023-09-28 00:07:05,248 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-03-01), DateFilter(op=operator.le, value=2020-05-31), DistanceFilter(op=operator.ge, value=0.05), DistanceFilter(op=operator.le, value=0.5), VelocityFilter(op=operator.ge, value=5), VelocityFilter(op=operator.le, value=25), DiameterFilter(op=operator.ge, value=0.5), DiameterFilter(op=operator.le, value=1.5)]
.2023-09-28 00:07:05,266 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.eq, value=2020-03-02)]
.2023-09-28 00:07:05,271 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.eq, value=2020-03-02), DistanceFilter(op=operator.le, value=0.4)]
.2023-09-28 00:07:05,277 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.eq, value=2020-03-02), DistanceFilter(op=operator.ge, value=0.1)]
.2023-09-28 00:07:05,282 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.eq, value=2020-03-02), DateFilter(op=operator.ge, value=2020-02-01), DateFilter(op=operator.le, value=2020-04-01)]
.2023-09-28 00:07:05,290 - database - INFO - Querying for close approaches with filters: [DateFilter(op=operator.ge, value=2020-10-01), DateFilter(op=operator.le, value=2020-04-01)]
.2023-09-28 00:07:05,296 - database - INFO - Querying for close approaches with filters: [HazardousFilter(op=operator.eq, value=True)]
.2023-09-28 00:07:05,300 - database - INFO - Querying for close approaches with filters: [DiameterFilter(op=operator.le, value=1.5)]
.2023-09-28 00:07:05,307 - database - INFO - Querying for close approaches with filters: [DiameterFilter(op=operator.ge, value=0.5), DiameterFilter(op=operator.le, value=1.5)]
.2023-09-28 00:07:05,312 - database - INFO - Querying for close approaches with filters: [DiameterFilter(op=operator.ge, value=1.5), DiameterFilter(op=operator.le, value=0.5)]
.2023-09-28 00:07:05,319 - database - INFO - Querying for close approaches with filters: [DistanceFilter(op=operator.le, value=0.4)]
.2023-09-28 00:07:05,323 - database - INFO - Querying for close approaches with filters: [DistanceFilter(op=operator.ge, value=0.1), DistanceFilter(op=operator.le, value=0.4)]
.2023-09-28 00:07:05,329 - database - INFO - Querying for close approaches with filters: [DistanceFilter(op=operator.ge, value=0.4), DistanceFilter(op=operator.le, value=0.1)]
.2023-09-28 00:07:05,334 - database - INFO - Querying for close approaches with filters: [VelocityFilter(op=operator.le, value=20)]
.2023-09-28 00:07:05,339 - database - INFO - Querying for close approaches with filters: [VelocityFilter(op=operator.ge, value=10), VelocityFilter(op=operator.le, value=20)]
.2023-09-28 00:07:05,345 - database - INFO - Querying for close approaches with filters: [VelocityFilter(op=operator.ge, value=20), VelocityFilter(op=operator.le, value=10)]
.2023-09-28 00:07:05,352 - database - INFO - Querying for close approaches with filters: [DiameterFilter(op=operator.ge, value=0.5)]
.2023-09-28 00:07:05,357 - database - INFO - Querying for close approaches with filters: [DistanceFilter(op=operator.ge, value=0.1)]
.2023-09-28 00:07:05,361 - database - INFO - Querying for close approaches with filters: [VelocityFilter(op=operator.ge, value=10)]
.2023-09-28 00:07:05,366 - database - INFO - Querying for close approaches with filters: [HazardousFilter(op=operator.eq, value=False)]
.2023-09-28 00:07:07,040 - models - INFO - Running time_str
2023-09-28 00:07:07,040 - models - INFO - Running time_str
2023-09-28 00:07:07,040 - models - INFO - Running time_str
2023-09-28 00:07:07,040 - models - INFO - Running time_str
2023-09-28 00:07:07,040 - models - INFO - Running time_str
....2023-09-28 00:07:08,782 - models - INFO - Running time_str
2023-09-28 00:07:08,782 - models - INFO - Running time_str
2023-09-28 00:07:08,782 - models - INFO - Running time_str
2023-09-28 00:07:08,782 - models - INFO - Running time_str
2023-09-28 00:07:08,782 - models - INFO - Running time_str
......
----------------------------------------------------------------------
Ran 73 tests in 9.843s

OK
```

## Save output to file
```bash
python main.py query --date 2020-01-01 --limit 5 --outfile output/5_csv_results.csv
python main.py query --date 2020-01-01 --limit 5 --outfile output/5_json_results.json
python main.py query --start-date 2020-01-01 --end-date 2020-12-31 --hazardous --min-diameter 0.25 --max-distance 0.1 --limit 5 --outfile output/results.json
```
