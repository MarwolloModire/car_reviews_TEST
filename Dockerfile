# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем Pipfile и Pipfile.lock в контейнер
COPY Pipfile* /app/

# Устанавливаем pipenv и зависимости
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

# Копируем весь проект в контейнер
COPY . /app/

# Переходим в директорию, где находится manage.py
WORKDIR /app/car_reviews

# Выполняем миграции и запускаем сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
