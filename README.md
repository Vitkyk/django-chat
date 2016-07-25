# django-chat
A twosome chat with lobby on Django

## System requirements

Ubuntu 14.04

python 2.7.6

```shell
$ pip install -r requirements.txt
```
### Run

Run django server:

```shell
$ python manage.py runserver
```
Run tornado server:

```
$ python chat/app.py
```

#### Environment variables

| Environment variable name |    Description      |                  Default value                    |
|---------------------------|---------------------|---------------------------------------------------|
|DJANGO_PORT                | Django Server Port  | 8000                                              |
|DJANGO_HOST                | Django Server Host  | 0.0.0.0                                           |
|TORNADO_PORT               | Tornado Server Port | 8888                                              |
|TORNADO_HOST               | Tornado Server Host | 0.0.0.0                                           |
| SECRET_KEY                | Django SECRET_KEY   |                                                   |
