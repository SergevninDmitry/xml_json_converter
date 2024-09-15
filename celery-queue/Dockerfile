FROM python:3.11.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /queue

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./celery-queue ./queue/