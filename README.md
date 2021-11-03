# Django-nginx-gunicorn

## Install to run on Django built-in engine:

```sh
git clone https://github.com/aleksef/django-gunicorn-nginx.git
```
```sh
cd django-gunicorn-nginx
```
```sh
virtualenv env
```
```sh
source env/bin/activate
```
```sh
pip install -r app/requirements.txt
```
#### Edit app/src/settings.py
```sh
SECRET_KEY = 'qwerty'
DEBUG = True
ALLOWED_HOSTS = []
```
```sh
cd app
```
```sh
python manage.py migrate
```
```sh
python manage.py runserver
```

## Install with Docker:

```sh
git clone https://github.com/aleksef/django-gunicorn-nginx.git
```
```sh
cd django-gunicorn-nginx
```
#### Edit app/src/settings.py
```sh
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
```
```sh
docker-compose build
```
```sh
docker-compose up -d
```

## Currently working links:
http://127.0.0.1:8000/accounts/login
http://127.0.0.1:8000/accounts/create_account
http://127.0.0.1:8000/accounts/settings
