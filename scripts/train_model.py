"""
Скрипт обучения ML-модели классификации заявок.

Запуск из корня проекта:
  python scripts/train_model.py

Или с указанием путей (опционально):
  python scripts/train_model.py --data data/labeled/labeled_requests.csv --output data/models/text_clf.pkl
"""

import argparse
import sys
from pathlib import Path

# Корень проекта — родитель папки scripts
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import Settings
from app.ml import MLModel


def main() -> None:
    parser = argparse.ArgumentParser(description="Обучение модели классификации заявок")
    parser.add_argument(
        "--data",
        type=Path,
        default=None,
        help="Путь к CSV с размеченными данными (по умолчанию из .env)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Путь для сохранения модели (по умолчанию из .env)",
    )
    parser.add_argument(
        "--text-column",
        type=str,
        default="text",
        help="Имя колонки с текстом",
    )
    parser.add_argument(
        "--label-column",
        type=str,
        default="label",
        help="Имя колонки с меткой",
    )
    args = parser.parse_args()

    config = Settings()
    data_path = args.data or config.labeled_data_path
    model_path = args.output or config.ml_model_path

    if not data_path.exists():
        print(f"Ошибка: файл с данными не найден: {data_path}")
        print("Убедитесь, что data/labeled/labeled_requests.csv существует.")
        sys.exit(1)

    print(f"Данные: {data_path}")
    print(f"Модель будет сохранена: {model_path}")

    model = MLModel(model_path)
    metrics = model.train(
        data_path,
        text_column=args.text_column,
        label_column=args.label_column,
    )

    print("\n--- Результаты обучения ---")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print("\nClassification report:")
    print(metrics["classification_report"])
    print(f"\nМодель сохранена: {model_path}")


if __name__ == "__main__":
    main()
