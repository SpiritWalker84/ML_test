"""Настройки приложения из переменных окружения (.env)."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Settings:
    """Класс настроек. Все значения загружаются из .env."""

    def __init__(self, env_file: Optional[str] = None) -> None:
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        # API
        self.api_key: str = self._get_required("API_KEY")
        self.openai_base_url: str = self._get("OPENAI_BASE_URL", "")
        self.llm_model: str = self._get("LLM_MODEL", "gpt-4o-mini")

        # Database
        self.database_url: str = self._get(
            "DATABASE_URL", "sqlite:///./data/app.db"
        )

        # Paths (относительно корня проекта)
        self.project_root: Path = self._project_root()
        self.labeled_data_path: Path = self.project_root / self._get(
            "LABELED_DATA_PATH", "data/labeled/labeled_requests.csv"
        )
        self.ml_model_path: Path = self.project_root / self._get(
            "ML_MODEL_PATH", "data/models/text_clf.pkl"
        )

        # Flask
        self.flask_env: str = self._get("FLASK_ENV", "development")
        self.flask_debug: bool = self._get("FLASK_DEBUG", "1").strip().lower() in ("1", "true", "yes")
        self.secret_key: str = self._get("SECRET_KEY", "dev-secret-change-in-production")
        self.port: int = int(self._get("PORT", "8082"))

    def _project_root(self) -> Path:
        """Корень проекта (папка, где лежит app/)."""
        return Path(__file__).resolve().parent.parent.parent

    def _get_required(self, key: str) -> str:
        value = os.getenv(key)
        if not value or not value.strip():
            raise ValueError(f"Переменная окружения {key} не установлена. Скопируйте .env.example в .env и заполните значения.")
        return value.strip()

    def _get(self, key: str, default: str) -> str:
        value = os.getenv(key, default)
        return value.strip() if value else default

    @property
    def openai_base_url_or_none(self) -> Optional[str]:
        """Base URL для OpenAI или None (использовать дефолтный)."""
        url = (self.openai_base_url or "").strip()
        return url if url else None
