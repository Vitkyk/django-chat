# django-chat
A twosome chat with lobby on Django

## System requirements

Ubuntu 14.04

python 2.7.6

Django 1.9.7

djangorestframework 3.4.0

tornado 4.4

### Run

1. Run django server: python manage.py runserver
2. Run tornado server: python chat/app.py

#### Environment variables

| Environment variable name |    Description      |                  Default value                    |
|---------------------------|---------------------|---------------------------------------------------|
|DJANGO_PORT                | Django Server Port  | 8000                                              |
|DJANGO_HOST                | Django Server Host  | 0.0.0.0                                           |
|TORNADO_PORT               | Tornado Server Port | 8888                                              |
|TORNADO_HOST               | Tornado Server Host | 0.0.0.0                                           |
| SECRET_KEY                | Django SECRET_KEY   | ra0tb@9cpw+6w$(i+gw!x_m1o8g3$4qo)ktp8!&+68-zq5p=v8|
