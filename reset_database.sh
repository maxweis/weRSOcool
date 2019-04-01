#!/bin/sh
rm ./db.sqlite3
sudo rm ./user/migrations -R
sudo rm ./rso_manage/migrations -R
rm -rf ./events/migrations
python3 ./manage.py migrate --run-syncdb
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@maxweis.com', 'admin')" | python3 ./manage.py shell

