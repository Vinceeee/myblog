#!/bin/bash

if [ ! -d migrations ];then
  rm -Rf migrations
  python manage.py db init
  python manage.py db upgrade
  python manage.py db migrate -m 'init'
fi
python manage.py deploy product
python manage.py deploy test_data

echo "Application start-up has been completed"
# python manage.py runserver -h 0.0.0.0 -p 5000
uwsgi uwsgi.ini

