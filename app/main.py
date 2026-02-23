"""Фабрика Flask-приложения: сборка модулей и регистрация маршрутов."""

from pathlib import Path

from flask import Flask

from app.config import Settings
from app.db import get_engine, get_session_factory, init_db
from app.ml import MLModel
from app.llm import LLMClient
from app.services import RequestAnalyzerService
from app.api import register_routes


def create_app(config: Settings | None = None) -> Flask:
    """Создать и сконфигурировать Flask-приложение."""
    if config is None:
        config = Settings()

    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent / "templates"),
    )
    app.config["SECRET_KEY"] = config.secret_key

    # БД
    engine = get_engine(config.database_url)
    init_db(engine)
    session_factory = get_session_factory(engine)

    # ML (ленивая загрузка при первом запросе)
    ml_model = MLModel(config.ml_model_path)

    # LLM
    llm_client = LLMClient(
        api_key=config.api_key,
        model=config.llm_model,
        base_url=config.openai_base_url_or_none,
    )

    # Сервис и маршруты
    analyzer = RequestAnalyzerService(ml_model, llm_client, session_factory)
    register_routes(app, analyzer)

    return app
