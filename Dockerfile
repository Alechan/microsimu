FROM python:3.8.3-buster

# Create user
RUN useradd --create-home --shell /bin/bash microsimu
ENV APP_HOME=/home/microsimu
WORKDIR $APP_HOME

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)
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

ENV STATIC_FILES_PATH=$APP_HOME/staticfiles
RUN mkdir $STATIC_FILES_PATH
RUN chown microsimu:microsimu $STATIC_FILES_PATH
VOLUME $STATIC_FILES_PATH
USER microsimu
