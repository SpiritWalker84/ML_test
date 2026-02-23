# AI-сервис заявок по банкротству
FROM python:3.12-slim

WORKDIR /app

# Зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код и данные
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY run.py wsgi.py ./
COPY data/labeled/ ./data/labeled/
RUN mkdir -p data/models

# Обучение модели при сборке (чтобы образ был готов к запуску)
RUN python scripts/train_model.py

# Порт приложения (переопределяется через PORT в .env)
ENV PORT=8082
EXPOSE 8082

# Gunicorn: 1 worker for small app; bind and workers overridable via env
ENV GUNICORN_WORKERS=2
ENV GUNICORN_THREADS=4
CMD ["sh", "-c", "gunicorn -w ${GUNICORN_WORKERS:-2} -b 0.0.0.0:${PORT:-8082} --threads ${GUNICORN_THREADS:-4} wsgi:app"]
