#!/bin/sh
rm ./db.sqlite3
rm -rf ./users/migrations
rm -rf ./rso_manage/migrations
rm -rf ./events/migrations
rm -rf ./wersocool/__pycache__
rm -rf ./users/__pycache__
rm -rf ./events/__pycache__
rm -rf ./rso_manage/__pycache__
python3 ./manage.py makemigrations users rso_manage events analytics
python3 ./manage.py migrate --run-syncdb
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@maxweis.com', 'admin')" | python3 ./manage.py shell
