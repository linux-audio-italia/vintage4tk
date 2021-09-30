# Vintage 4tk cassette recorders

A website to collect vintage 4 tracks cassette recorders.

## Local development setup

1. Copy and customize Django settings (especially https://docs.djangoproject.com/en/3.2/ref/settings/#databases)

```
$ cp vintage4tk/settings/ci.py vintage4tk/settings/local.py
$ $EDITOR vintage4tk/settings/local.py
```

2. Create a virtualenv and install the requirements

```
$ python -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
```

3. Create the database and migrate the schema

```
$ createdb <dbname> --owner=<dbowner>
$ python manage.py migrate
```

4. Load some test data

```
$ python manage.py loaddata users brands recorders
```

5. Run the development server

```
$ python manage.py runserver
```

The admin username and password are **admin** / **adminadmin**.

Visit the website at http://127.0.0.1:8000
and the admin interface at http://127.0.0.1:8000/admin

