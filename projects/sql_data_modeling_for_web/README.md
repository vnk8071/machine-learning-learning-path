# Fyyur

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Overview

This app is nearly complete. It is only missing one thing… real data! While the views and controllers are defined in this application, it is missing models and model interactions to be able to store retrieve, and update data from a database. By the end of this project, you should have a fully functioning site that is at least capable of doing the following, if not more, using a PostgreSQL database:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

## Installation
```bash
pip install -r requirements.txt
```

## Run Application
```bash
FLASK_APP=app FLASK_ENV=development flask run
```

Result:
```
11:17:41
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

## Home Page
Route: 'localhost:5000/'

![home](images/homepage.png)

## Venues Page
![venue_page](images/venue_page.png)
### Insert Data
![post_venue](images/post_venue.png)

Then, insert successfully:
![post_venue_success](images/post_venue_success.png)

### Edit Data
![venue_edit](images/venue_edit.png)

### Search Data
![venue_search](images/venue_search.png)

### Detail Data
![venue_detail_page](images/venue_detail_page.png)

### Upcoming Shows
![show_venue_upcoming](images/show_venue_upcoming.png)

### Venues Database
![psql_venue](images/pqsl_venue.png)

```sql
 id |          name          |     city      | state |       address       |    phone     |                                                              image_link                                                               |               facebook_link               | seeking_talent |                                seeking_description                                |           website_link           |           genres
----+------------------------+---------------+-------+---------------------+--------------+---------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------+----------------+-----------------------------------------------------------------------------------+----------------------------------+----------------------------
  1 | The Musical Hop        | San Francisco | CA    | 1015 Folsom Street  | 123-123-1234 | https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60    | https://www.facebook.com/TheMusicalHop    | t              | We are on the lookout for a local artist to play every two weeks. Please call us. | https://www.themusicalhop.com    | Classical,Folk,Jazz,Reggae
  2 | The Dueling Pianos Bar | New York      | NY    | 335 Delancey Street | 914-003-1132 | https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80 | https://www.facebook.com/theduelingpianos | f              |                                                                                   | https://www.theduelingpianos.com | Classical,Hip-Hop,R&B
(2 rows)
```

## Artists Page
![artist_page](images/artist_page.png)

### Insert Data
![post_artist](images/post_artist.png)

Then, insert successfully:
![post_artist_success](images/post_artist_success.png)

### Edit Data
![artist_edit](images/artist_edit.png)

### Search Data
![artist_search](images/artist_search.png)

### Detail Data
![artist_detail_page](images/artist_detail_page.png)

### Upcoming Shows
![show_artist_upcoming](images/show_artist_upcoming.png)

### Artists Database
![psql_artist](images/psql_artist.png)

```sql
 id |     name      |     city      | state |    phone     |   genres    |                                                             image_link                                                             |            facebook_link             |          website_link           | seeking_venue |                      seeking_description
----+---------------+---------------+-------+--------------+-------------+------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+---------------------------------+---------------+----------------------------------------------------------------
  1 | Guns N Petals | San Francisco | CA    | 326-123-5000 | Rock n Roll | https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80 | https://www.facebook.com/GunsNPetals | https://www.gunsnpetalsband.com | t             | Looking for shows to perform at in the San Francisco Bay Area!
(1 row)
```

## Shows Page
![show_page](images/show_page.png)

### Insert Data
![post_show](images/post_show.png)

Then, insert successfully:
![post_show_success](images/post_show_success.png)

### Shows Database
![psql_show](images/psql_show.png)

```sql
 id |     start_time      | artist_id | venue_id
----+---------------------+-----------+----------
  1 | 2023-10-05 11:18:42 |         1 |        1
  2 | 2023-10-05 15:18:42 |         1 |        2
(2 rows)
```

## Migration
### Initial migration
```bash
flask db init
```

Result:
```
Creating directory '/Users/macos/projects/Kelvin/cd0046-SQL-and-Data-Modeling-for-the-Web/migrations' ...  done
Creating directory '/Users/macos/projects/Kelvin/cd0046-SQL-and-Data-Modeling-for-the-Web/migrations/versions' ...  done
Generating /Users/macos/projects/Kelvin/cd0046-SQL-and-Data-Modeling-for-the-Web/migrations/script.py.mako ...  done
Generating /Users/macos/projects/Kelvin/cd0046-SQL-and-Data-Modeling-for-the-Web/migrations/env.py ...  done
Generating /Users/macos/projects/Kelvin/cd0046-SQL-and-Data-Modeling-for-the-Web/migrations/README ...  done
Generating /Users/macos/projects/Kelvin/cd0046-SQL-and-Data-Modeling-for-the-Web/migrations/alembic.ini ...  done
Please edit configuration/connection/logging settings in '/Users/macos/projects/Kelvin/cd0046-SQL-and-Data-Modeling-for-the-Web/migrations/alembic.ini' before proceeding.
```

### Migrate
```bash
flask db migrate
```

Check in `migrations/versions/` for the migration file.

Result:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'artists'
INFO  [alembic.autogenerate.compare] Detected added table 'venues'
INFO  [alembic.autogenerate.compare] Detected added table 'shows'
  Generating /Users/macos/projects/Kelvin/cd0046-SQL-and-Data-Modeling-for-the-Web/migrations/versions/256536967864_.py ...  done
```
