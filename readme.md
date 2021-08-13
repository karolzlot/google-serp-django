## Google Serp web app written in Python & Django

It is my first attempt to make app with Django. And I liked it. I was using only Flask and FastAPI before.

Tested on python 3.9


How to run this app
1. Rename `.env.example` to `.env`. This file contains environmental variables.
2. In `.env` file fill at least `SECRET_KEY` with some random characters, it is used internally by Django.
3. (Optionally) Fill `.env` with credentials to your Postgres database.

Then you can run this app by creating virtual environment or by starting docker.


### A. Running in Docker:
(You need to fill Postgres db credentials to `.env` file in this case, this Docker method doesn't work with sqlite)

1. Build and run Docker:
```
docker build . --tag google-serp-django
docker run --env-file .env -p 8080:8080 google-serp-django
```
2. Go to app address:
http://localhost:8080/






### B. Running in virtual environment:
1. Create virtual env for this project.
```
python -m venv .venv --prompt google-serp-django
.\.venv\Scripts\python -m pip install -U pip
.\.venv\Scripts\python -m pip install -U wheel
.\.venv\Scripts\pip install -r requirements.txt
````

2. Run app (two options)

    - Run with new local sqlite db:
    ```
    python manage.py makemigrations serp_app --settings=mysite.settings.local_sqlite
    python manage.py migrate --settings=mysite.settings.local_sqlite
    python manage.py runserver --settings=mysite.settings.local_sqlite
    ```

    - Run with your postgres db:
    ```
    python manage.py makemigrations serp_app --settings=mysite.settings.cloud_postgres
    python manage.py migrate --settings=mysite.settings.cloud_postgres
    python manage.py runserver --settings=mysite.settings.cloud_postgres
    ```

3. Go to app address:
http://localhost:8080/



## Details about project decisions

### Transactions:

I set `ATOMIC_REQUESTS` to `True`

However this setting is not good idea under heavy load. In that case I would specify transactions manually.

### @dataclass in `search_result.py`

I added `Dataclass` to names of dataclass objects, so those are different from names in `models.py`. They could be easily mistaken otherwise.

### File `google_search.py` 

As `GoogleSearch()` class doesn't have any state, I decided to make it a class with `@staticmethod` methods only. 

This practice is a bit controversial, because I could just remove class and leave only bunch of functions in this file. But in my opinion class with static methods looks a little nicer, so I left it this way. It's just personal preference.

### File `view.py` 

I wonder if it is possible to make calls to db in this file simpler. They are now quite spacious unfortunately.


### UTC
In database I save datatime only as timezone-aware (in other words it is UTC-only datetime).

### Postgres

Sqlite databases are not easy to use in dockerized environment. I switched to Postgres for deployment in Cloud. Therefore I divided settings to be able to use those both databases.

### Type hinting

I use it in some places, but I still am not familiar enough to use it everywhere.


## What could be improved in this project (if I could find time):

- add support of proxies
- validation of form fields
- better saving of last state of form fields, so user don't need to repeat entering settings
- change of server in Dockerfile from internal django server to faster `asgi` server, e.g. `Uvicorn`
- choice of google search domain and language, currently those are hard-coded to Polish version of google search
- handling of cookies and better coping with robot detection
