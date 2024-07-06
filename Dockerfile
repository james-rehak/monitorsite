FROM python:3.11-bullseye

ENV PYTHONBUFFERED=1

WORKDIR /monitorsite

RUN apt-get update && apt-get -y install default-libmysqlclient-dev

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN  chmod +x manage.py

#CMD python manage.py runserver 0.0.0.0:8000

