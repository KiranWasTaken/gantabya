Stage 1: Build environment
FROM python:3.10-slim as builder
FROM hereshem/python:django4.2.15 AS builder
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
Create an empty .env file
RUN touch .env

FROM builder AS test
RUN python3 manage.py makemigrations
RUN python3 manage.py test apps

FROM builder AS main
RUN python manage.py collectstatic --noinput
CMD to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "config.wsgi", "--bind","0.0.0.0:8000","--log-file","/logs"]
CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--log-level", "debug"]