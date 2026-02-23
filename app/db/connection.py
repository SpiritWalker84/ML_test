"""Подключение к БД и фабрика сессий."""

from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models import Base


def get_engine(database_url: str, echo: bool = False):
    """Создать движок SQLAlchemy."""
    # SQLite требует connect_args для относительного пути
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(
        database_url,
        echo=echo,
        connect_args=connect_args,
        future=True,
    )


def get_session_factory(engine):
    """Фабрика сессий."""
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def init_db(engine) -> None:
    """Создать таблицы."""
    Base.metadata.create_all(bind=engine)


def get_session(session_factory) -> Session:
    """Вернуть новую сессию (контекстный менеджер — вызывающий код сам close)."""
    return session_factory()
