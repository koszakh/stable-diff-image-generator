# Используем Python 3.10
FROM python:3.10

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Копируем код проекта
COPY . .

RUN mkdir -p /app/media/generated

# Команда по умолчанию (будет переопределена в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
