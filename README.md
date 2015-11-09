
# interpreteer #

## About ##

Helps bringing newcomers, translators and interpreters together.

volunteer + interpreter = interpreteer!

http://www.interpreteer.de/

## Prerequisites ##

- Python 2.7
- pip
- virtualenv (virtualenvwrapper is recommended for use during development)

## Installation ##

``` bash
pip install -r requirements.txt
python manage.py migrate
python manage.py add_langs_to_db
python manage.py loaddata fixtures/seed #load seed data
python manage.py runserver
```
