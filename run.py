"""Точка входа: запуск Flask-приложения."""

import os
from pathlib import Path

# Корень проекта — текущая директория или родительская к run.py
ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

from app.main import create_app
from app.config import Settings

if __name__ == "__main__":
    config = Settings()
    app = create_app(config)
    app.run(
        host="0.0.0.0",
        port=config.port,
        debug=config.flask_debug,
    )
