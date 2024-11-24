# Используем официальный образ Python с нужной версией
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем только файлы зависимостей для кэширования слоев Docker
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости проекта без dev-зависимостей
RUN poetry install --no-root --no-dev

# Копируем остальной код приложения
COPY . /app

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=hw_flask/main.py

# Открываем порт, на котором работает ваше приложение
EXPOSE 5000

# Команда для запуска вашего приложения с использованием Gunicorn с автоматической перезагрузкой
CMD ["poetry", "run", "gunicorn", "--reload", "-b", "0.0.0.0:5000", "hw_flask.main:app"]
