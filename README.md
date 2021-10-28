<div align="center" style="padding-bottom: 10px">
    <h1>Bowell Backend</h1>
    <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray" alt=""/>
    <img src="https://img.shields.io/badge/Celery-8C9A41?&style=for-the-badge&logo=celery&logoColor=Awhite" alt=""/>
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Docker-008FCC?style=for-the-badge&logo=docker&logoColor=white" alt=""/>
</div>

## Tools, libraries, frameworks:
This setup has been tested with Python 3.9.

### Backend
- Django + Django Rest Framework : `django` `djangorestframework`
- Django Channels 3 : `channels`- handling websockets backend
- `django-cors-headers` - handling cross origin requests
- `coverage` - for code coverage reports and running unit tests
- `mypy` + `djangorestframework-stubs` - for better typing experience
- `psycopg2` - needed to use Postgres (in Docker container)
- `channels_redis`, `redis` - connection to Redis database service
- `daphne` - production asgi server
- `whitenoise` - building static files for production
- `celery` - task queue
- `drf-yasg` - OpenAPI documentation

## Development setup:
Environmental variables in .env (random values below)
```
SECRET_KEY=longrandomlygeneratedsecretkey
DB_NAME=postgresdbname
DB_USER=postgresusername
DB_PASSWORD=postgrespassword
PG_ADMIN_EMAIL=pgadminemail@x.y
PG_ADMIN_PASSWORD=pgadminpassword
```


### Without Docker
Create a virtual environment
```shell script
py -3 -m venv venv

venv/Scripts/Activate

python -m pip install --upgrade pip

pip install -r requirements.txt
```

Run django application
```shell script
python manage.py runserver
```

Preparing (if there are any changes to db schema) and running migrations
```shell script
python manage.py makemigrations

python manage.py migrate
```

Create superuser
```shell script
python manage.py createsuperuser
```

### Tests coverage
Run tests using Coverage
```shell script
coverage run manage.py test
```
Get report from coverage:
```shell script
coverage report -m
```

## With Docker
**IMPORTANT**:
- Change line endings in shell scripts from CRLF to LF
- Remove twisted-iocpsupport from requirements.txt if present
- Remember about env variables

Make sure Docker Engine is running.  

While in **root directory**, build docker images and run them with docker-compose. This might take up to few minutes. 
Rebuilding image is crucial after installing new packages via pip.

```shell script
docker-compose up --build
```

Application should be up and running: backend `127.0.0.1:8000`.

If docker images are installed and **no additional packages have been installed**, just run to start containers:
```shell script
docker-compose up
```

Bringing down containers
```shell script
docker-compose down
```

To run commands in an active container:
```shell script
docker exec -it <container_id/container_name> <command>
```

e.g
```shell
docker exec -it backend python manage.py migrate
docker exec -it backend python manage.py shell
docker exec -it backend bash
```
