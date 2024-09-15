FROM python:3.11.3
# Установка рабочей директории внутри контейнера
WORKDIR /api

# Установка зависимостей
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt


COPY ./api ./api/
# Устанавливаем netcat для проверки базы данных
RUN apt-get update && apt-get install -y netcat

# Делаем entrypoint исполняемым
RUN chmod +x ./api/entrypoint.sh

# Указание абсолютного пути к модулю Flask-приложения
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "3", "app:flask_app"]

ENTRYPOINT ["/api/entrypoint.sh"]
