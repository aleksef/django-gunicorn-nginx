#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# migrate and collect static
rm -r -f mediafiles/
python manage.py migrate
python manage.py collectstatic --no-input --clear
# create admin user
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'qgfwjcxn')" | python manage.py shell

exec "$@"