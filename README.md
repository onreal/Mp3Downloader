# Mp3Downloader

Mp3Downloader is a Python Flask App for converting youtube videos to mp3. Also have an integrated telegram bot in order to download music directly on any device, also the bot support inline search for rapid results.

## Demo

There is currently an active Telegram Bot where you can try this project. Just search for [Mp3Father](https://t.me/EasyMp3Bot)

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

## Start Projects

### Telegram Chat Bot
```bash
venv/bin/python3.7 app/bot/Mp3TelegramBot.py
```

### Telegram Message Broadcaster
```bash
venv/bin/python3.7 app/bot/Mp3TelegramBot.py
```

### Flask Web Site for searching MP3s
```bash
venv/bin/python3.7 app/__init__.py
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
PYTHONPATH=/venv/lib/python3.7/site-packages
FLASK_APP=app/__init__.py
```

## TODO
    - Code optimisations on varius places
    - Bot Admin Front-End
    - Broadcaster to get messages from PostgresSQL
    - Many many other things, will keep this list updated :)

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
