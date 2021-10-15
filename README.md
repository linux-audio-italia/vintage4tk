# Vintage 4tk cassette recorders

A website to collect vintage 4 tracks cassette recorders.

![example workflow](https://github.com/linux-audio-italia/vintage4tk/actions/workflows/CI.yml/badge.svg)
[![Code style: djLint](https://img.shields.io/badge/html%20style-djLint-blue.svg)](https://github.com/Riverside-Healthcare/djlint)
[![Code style: black](https://img.shields.io/badge/python%20style-black-000000.svg)](https://github.com/psf/black)
[![CSS style: stylelint](https://img.shields.io/badge/css%20style-stylelint-yellowgreen)](https://stylelint.io/)

## Local development setup

1. Copy and customize Django settings (especially https://docs.djangoproject.com/en/3.2/ref/settings/#databases)

```
$ cp vintage4tk/settings/ci.py vintage4tk/settings/local.py
$ $EDITOR vintage4tk/settings/local.py
```

2. Create a virtualenv and install the python and node requirements

```
$ python -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
$ npm install
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

5. Run the development server and css compilation

```
$ supervisord
```

Visit the website at http://127.0.0.1:8000
and the admin interface at http://127.0.0.1:8000/admin

The admin username and password are **admin** / **adminadmin**.
