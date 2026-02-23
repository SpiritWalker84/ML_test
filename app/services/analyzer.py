"""Сервис обработки заявки: ML-классификация + LLM резюме/поля + сохранение в БД."""

from typing import Any, Optional

from app.db import Request, get_session_factory
from app.ml import MLModel
from app.llm import LLMClient


class RequestAnalyzerService:
    """Обработка одной заявки: классификация, резюме, извлечение полей, сохранение."""

    def __init__(
        self,
        ml_model: MLModel,
        llm_client: LLMClient,
        session_factory,
    ) -> None:
        self.ml_model = ml_model
        self.llm_client = llm_client
        self.session_factory = session_factory

    def analyze(self, text: str, save: bool = True) -> dict[str, Any]:
        """
        Обработать текст заявки.
        Возвращает label, confidence, summary, fields; при save=True сохраняет в БД.
        """
        text = (text or "").strip()
        if not text:
            return {
                "error": "Текст заявки не может быть пустым",
                "label": None,
                "confidence": None,
                "summary": None,
                "fields": None,
            }

        ml_result = self.ml_model.predict(text)
        summary = self.llm_client.summarize_request(text)
        fields = self.llm_client.extract_fields(text)

        record_id: Optional[int] = None
        if save:
            session = self.session_factory()
            try:
                req = Request(
                    raw_text=text,
                    label=ml_result["label"],
                    summary=summary,
                    extracted=fields,
                )
                session.add(req)
                session.commit()
                session.refresh(req)
                record_id = req.id
            finally:
                session.close()

        return {
            "id": record_id,
            "label": ml_result["label"],
            "confidence": ml_result["confidence"],
            "summary": summary,
            "fields": fields,
        }
