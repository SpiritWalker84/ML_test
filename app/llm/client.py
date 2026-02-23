"""Клиент для работы с LLM API (OpenAI-совместимый, в т.ч. через прокси)."""

import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)


class LLMClientBase(ABC):
    """Базовый интерфейс LLM-клиента."""

    @abstractmethod
    def complete(self, prompt: str, temperature: float = 0.3) -> Optional[str]:
        """Отправить промпт и вернуть текст ответа."""
        pass


class LLMClient(LLMClientBase):
    """Клиент OpenAI-совместимого API (прямой OpenAI или прокси, например api.proxyapi.ru)."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        base_url: Optional[str] = None,
    ) -> None:
        self.api_key = api_key
        self.model = model
        kwargs = {"api_key": api_key}
        if base_url and base_url.strip():
            kwargs["base_url"] = base_url.rstrip("/")
        self._client = OpenAI(**kwargs)

    def complete(self, prompt: str, temperature: float = 0.3) -> Optional[str]:
        """Один запрос (user message) — возврат текста ответа."""
        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            if resp.choices and len(resp.choices) > 0:
                return (resp.choices[0].message.content or "").strip()
        except Exception as e:
            logger.exception("LLM API call failed: %s", e)
        return None

    def summarize_request(self, text: str) -> str:
        """Краткое резюме заявки для юриста (3–4 предложения)."""
        prompt = (
            "Клиент описывает свою долговую ситуацию. "
            "Сделай краткое резюме для юриста (3–4 предложения), без выдумывания фактов.\n\n"
            f"Текст клиента:\n{text}\n\nРезюме:"
        )
        result = self.complete(prompt, temperature=0.3)
        return result or "(не удалось сформировать резюме)"

    def extract_fields(self, text: str) -> dict[str, Any]:
        """Извлечь из текста: total_debt, creditors_count, has_overdue, notes."""
        prompt = (
            "Проанализируй текст и верни JSON с ключами: "
            '"total_debt" (число или null), '
            '"creditors_count" (число или null), '
            '"has_overdue" (true/false), '
            '"notes" (краткий комментарий). '
            "Только JSON, без пояснений.\n\n"
            f"Текст клиента:\n{text}\n\nJSON:"
        )
        result = self.complete(prompt, temperature=0.2)
        if not result:
            return {"raw_response": None}
        try:
            # Убрать возможные markdown-обёртки
            raw = result.strip()
            if raw.startswith("```"):
                lines = raw.split("\n")
                raw = "\n".join(
                    line for line in lines
                    if not line.strip().startswith("```")
                )
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"raw_response": result}
