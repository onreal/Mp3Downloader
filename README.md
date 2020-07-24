# Mp3Downloader

Mp3Downloader is a Python Flask App for converting youtube videos to mp3. Also have an integrated telegram bot in order to download music directly on any device, also the bot support inline search for rapid results.

## Store
PostgreSql is required in order to store data that are required from the program. 

## Installation

Create Python virtual environment

```bash
python3.7 -m venv venv
```

Install project requirement

```bash
venv/bin/pip3.7 install -r requirements.txt
```

Setup project with setuptools

```bash
venv/bin/python3.7 setup.py install
```

## Database migration

Update configuration file

```bash
nano app/config.py
```

Postgres migration

```bash
venv/bin/python3.7 app/scripts/migrate_pgsql.py db init
venv/bin/python3.7 app/scripts/migrate_pgsql.py db migrate
venv/bin/python3.7 app/scripts/migrate_pgsql.py db upgrade
```

## Environment

```bash
PATH=$PATH
APP_SETTINGS="config.DevelopmentConfig"
PGSQL_CONNECTION_STRING="postgres://username:password@host:port/database"
PYTHONPATH=/wproject/venv/lib/python3.7/site-packages
FLASK_APP=app/__init__.py
```

## TODO

 - Many things :)

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)