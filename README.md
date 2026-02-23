# AI-сервис для обработки заявок по банкротству

Учебный проект: первичная обработка текстовых заявок (NLP + LLM). Классификация типа заявки, извлечение параметров и резюме для юриста.

## Стек

- Python 3.10+
- Flask, SQLAlchemy (SQLite/PostgreSQL)
- scikit-learn (TfidfVectorizer + LogisticRegression)
- OpenAI-совместимый API (OpenAI или прокси)

## Структура проекта (модульная, ООП)

```
Project C/
├── app/
│   ├── config/          # Настройки из .env (Settings)
│   ├── db/               # Модели и подключение к БД
│   ├── ml/               # ML-модель классификации (MLModel)
│   ├── llm/              # Клиент LLM (LLMClient)
│   ├── services/         # Сервисный слой (RequestAnalyzerService)
│   ├── api/              # Маршруты Flask
│   ├── templates/
│   └── main.py           # Фабрика приложения
├── data/
│   ├── labeled/         # labeled_requests.csv (пример уже есть)
│   └── models/          # text_clf.pkl после обучения
├── scripts/
│   └── train_model.py   # Обучение модели: python scripts/train_model.py
├── tests/
├── .env.example
├── .env                 # не в git — создать из .env.example
├── requirements.txt
├── run.py               # Запуск: python run.py
├── Dockerfile
├── docker-compose.yml   # порт 8082
└── README.md
```

## Быстрый старт

1. **Клонировать / перейти в каталог проекта.**

2. **Создать виртуальное окружение и зависимости:**
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. **Настроить окружение:**
   ```bash
   copy .env.example .env   # Windows
   # Отредактировать .env: указать API_KEY (и при необходимости OPENAI_BASE_URL)
   ```

4. **Обучить модель (один раз):**  
   В проекте уже есть пример данных `data/labeled/labeled_requests.csv` (60 заявок, 3 класса: консультация, подготовка_документов, подача_заявления). Запуск обучения:
   ```bash
   python scripts/train_model.py
   ```
   Опционально: другие пути к данным и модели:
   ```bash
   python scripts/train_model.py --data data/labeled/labeled_requests.csv --output data/models/text_clf.pkl
   ```

5. **Запустить приложение:**
   ```bash
   python run.py
   ```
   Открыть в браузере: http://127.0.0.1:8082 (порт задаётся через `PORT` в .env, по умолчанию 8082).

## Docker

Порт **8082** выведен наружу.

1. Создать `.env` из `.env.example` и указать `API_KEY`.
2. Собрать и запустить:
   ```bash
   docker compose up --build
   ```
   Или только сборка и запуск в фоне:
   ```bash
   docker compose build && docker compose up -d
   ```
3. Открыть: http://localhost:8082

При сборке образа модель обучается автоматически (`RUN python scripts/train_model.py`). БД SQLite монтируется в `./data/app.db` на хосте.

## API

- **GET /** — форма ввода текста заявки.
- **POST /analyze** — отправка формы, ответ — HTML с результатом.
- **POST /api/analyze** — JSON: `{"text": "..."}` → `{"label", "confidence", "summary", "fields"}`.

## Переменные окружения (.env)

См. `.env.example`. Обязательно: `API_KEY`. Остальное опционально (есть значения по умолчанию).
