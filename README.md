
# interpreteer #

## About ##

Helps bringing newcomers, translators and interpreters together.

volunteer + interpreter = interpreteer!

http://www.interpreteer.de/

## Prerequisites ##

- Python 2.7, 3.4 recommended
- pip
- virtualenv (virtualenvwrapper is recommended for use during development)

## Installation ##

``` bash
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/seed #load seed data
python manage.py runserver
```
