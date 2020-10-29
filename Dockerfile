FROM python:3.8.3-buster

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# system dependencies
RUN apt-get update \
    && apt-get -y install postgresql gcc python3-dev musl-dev

# python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src .

RUN python manage.py makemigrations
RUN python manage.py migrate
