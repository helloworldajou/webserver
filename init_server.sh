#!/usr/bin/env bash
sudo cp nginx.conf /etc/nginx/sites-enabled/
service postgresql start
service nginx restart
psql -U postgres < "./init_db.sql"
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000