"""
Скрипт обучения ML-модели классификации заявок.

Не требует API_KEY или .env — только пути к данным (или аргументы).
При сборке Docker вызывается без .env.

Запуск из корня проекта:
  python scripts/train_model.py

Или с указанием путей (опционально):
  python scripts/train_model.py --data data/labeled/labeled_requests.csv --output data/models/text_clf.pkl
"""

import argparse
import os
import sys
from pathlib import Path

# Корень проекта — родитель папки scripts
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.ml import MLModel


def main() -> None:
    parser = argparse.ArgumentParser(description="Обучение модели классификации заявок")
    parser.add_argument(
        "--data",
        type=Path,
        default=None,
        help="Путь к CSV с размеченными данными",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Путь для сохранения модели",
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

    data_path = args.data or ROOT / os.getenv("LABELED_DATA_PATH", "data/labeled/labeled_requests.csv")
    model_path = args.output or ROOT / os.getenv("ML_MODEL_PATH", "data/models/text_clf.pkl")
    # Нормализуем пути (если заданы относительные — от ROOT)
    if not data_path.is_absolute():
        data_path = ROOT / data_path
    if not model_path.is_absolute():
        model_path = ROOT / model_path

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
