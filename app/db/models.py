"""Модели SQLAlchemy для хранения заявок."""

from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Request(Base):
    """Обработанная заявка клиента."""

    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    raw_text = Column(Text, nullable=False)
    label = Column(String(50), nullable=True)  # класс от ML
    summary = Column(Text, nullable=True)      # резюме от LLM
    extracted = Column(JSON, nullable=True)  # поля от LLM (dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "raw_text": self.raw_text[:200] + "..." if len(self.raw_text or "") > 200 else (self.raw_text or ""),
            "label": self.label,
            "summary": self.summary,
            "extracted": self.extracted,
        }
