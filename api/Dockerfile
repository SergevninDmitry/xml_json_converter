FROM python:3.11.3

WORKDIR /api

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt


COPY ./api ./api/

RUN apt-get update && apt-get install -y netcat

RUN chmod +x ./api/entrypoint.sh

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "3", "app:flask_app"]

ENTRYPOINT ["/api/entrypoint.sh"]
