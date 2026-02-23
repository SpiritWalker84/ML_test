# AI-сервис заявок по банкротству

Веб-сервис для первичной обработки текстовых заявок: классификация типа заявки (консультация / подготовка документов / подача заявления), извлечение параметров (сумма долга, количество кредиторов, просрочки) и формирование краткого резюме для юриста.

**Технологии:** Python, Flask, SQLAlchemy (SQLite), scikit-learn (TfidfVectorizer + LogisticRegression), OpenAI-совместимый API, Gunicorn, Docker.

## Запуск (Docker)

```bash
cp .env.example .env   # указать API_KEY
docker compose up --build
```

Сервис: http://localhost:8082

Переменные окружения — см. `.env.example` (обязателен `API_KEY`).
