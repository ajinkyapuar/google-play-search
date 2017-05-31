#Google Play Search

URL: http://localhost:8000/searchapp

RUN SERVER: python manage.py runserver

- django-admin startproject googlePlaySearch
- python manage.py migrate
- python manage.py runserver
- python manage.py startapp searchapp
- python manage.py makemigrations searchapp 
- python manage.py sqlmigrate searchapp 0001

