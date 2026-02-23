"""Класс ML-модели: обучение и предсказание типа заявки."""

from pathlib import Path
from typing import Any, Optional

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


class MLModel:
    """Пайплайн классификации текста (TfidfVectorizer + LogisticRegression)."""

    def __init__(self, model_path: Path) -> None:
        self.model_path = Path(model_path)
        self._pipeline: Optional[Pipeline] = None

    def train(
        self,
        data_path: Path,
        text_column: str = "text",
        label_column: str = "label",
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> dict[str, Any]:
        """
        Обучить модель на размеченных данных.
        Возвращает словарь с метриками (accuracy, report).
        """
        df = pd.read_csv(data_path)
        X = df[text_column].astype(str)
        y = df[label_column]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer()),
            ("clf", LogisticRegression(max_iter=1000)),
        ])
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, self.model_path)
        self._pipeline = pipeline

        return {
            "accuracy": accuracy,
            "classification_report": report,
        }

    def load(self) -> "MLModel":
        """Загрузить модель с диска."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Модель не найдена: {self.model_path}. Сначала выполните обучение.")
        self._pipeline = joblib.load(self.model_path)
        return self

    @property
    def pipeline(self) -> Pipeline:
        """Пайплайн (загружается при первом обращении)."""
        if self._pipeline is None:
            self.load()
        return self._pipeline

    def predict(self, text: str) -> dict[str, Any]:
        """
        Предсказать класс заявки.
        Возвращает {"label": str, "confidence": float или None}.
        """
        pl = self.pipeline
        # predict ожидает итерируемый объект
        label = pl.predict([text])[0]
        proba = None
        if hasattr(pl, "predict_proba"):
            proba = float(pl.predict_proba([text])[0].max())
        return {"label": str(label), "confidence": proba}
