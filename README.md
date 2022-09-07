# News API
This repository provides sources for the django web-application for reading and managing news.
## Features
- Application based on celery periodic tasks which allows constantly update data
- Admin LTE 3 for admin managing news and users
- API which allows collect news by given date or tags
# Tech
- Python
- Django
- DRF
- Celery
- django_celery_beat
- AdminLTE 3
- Docker
- PostgreSQL
# Deploy manually
## Requirements
- PostgreSQL
- Python + pipenv
## Prepare
In project directory install all necessary python libraries:
```bash
pipenv install --system --deploy --ignore-pipfile
```
Initialize PostgreSQL with init.sql
```bash
psql -U postgres -f init.sql
```
## Run
Activate pipenv in each terminal:
```bash
pipenv shell
```
Run celery-beat and celery-worker in separate terminals:
- Beat
```bash
celery -A newsAPI beat -l info
```
- Worker
```bash
celery -A newsAPI worker -l info
```
Run python django server:
```bash
python manage.py runserver
```
# Deploy with Docker
You can deploy with web-application with docker container:
```bash
docker-compose up --build -d
```
View all running containers:
```bash
docker ps -a
```
Stop containers:
```bash
docker-compose down -v
```
View logs:
```bash
docker logs --tail {amount of lines} --follow --timestamps {container name}
```
# Usage
To use Admin LTE 3 go to http://localhost:8000
Frontend-endpoints located at http://localhost:8000/news/date and http://localhost:8000/news/tags

Date represents string in format "Days Month(on Russian) Year"

Tags represents array such as Yandex, Ozon, FBS

You should pass date and tags parameters in http-query, examples:
- "http://localhost:8000/news/date?date=7 сентября 2022"
- "http://localhost:8000/news/tags?tags=Yandex,Ozon"