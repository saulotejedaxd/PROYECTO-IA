"""
ArduinoBot - Entrenamiento del clasificador de intenciones.
Autor: Saulo Jaziel Tejeda Valle
Registro: 23310404

Este archivo lee data/intents.json, genera ejemplos de entrenamiento y guarda
un modelo de Machine Learning para clasificar dudas comunes sobre Arduino.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "intents.json"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "arduino_intent_model.joblib"
RESPONSES_PATH = MODEL_DIR / "responses.joblib"


def load_training_data(path: Path = DATA_PATH) -> Tuple[List[str], List[str], dict]:
    """Carga patrones, etiquetas y respuestas desde el archivo JSON."""
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    texts: List[str] = []
    labels: List[str] = []
    responses = {}

    for intent in data["intents"]:
        tag = intent["tag"]
        responses[tag] = intent["responses"]
        for pattern in intent["patterns"]:
            texts.append(pattern)
            labels.append(tag)

    return texts, labels, responses


def build_pipeline() -> Pipeline:
    """Crea el pipeline TF-IDF + Regresión Logística."""
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 2),
                    min_df=1,
                ),
            ),
            (
                "classifier",
                LinearSVC(
                    class_weight="balanced",
                    random_state=42,
                    max_iter=5000,
                ),
            ),
        ]
    )


def train() -> None:
    """Entrena y guarda el modelo."""
    texts, labels, responses = load_training_data()
    pipeline = build_pipeline()

    # El dataset es pequeño, así que la evaluación se hace como evidencia educativa.
    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )

    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    # Para el archivo final se reentrena con todos los ejemplos disponibles.
    # La evaluación anterior queda como evidencia educativa.
    pipeline.fit(texts, labels)

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    joblib.dump(responses, RESPONSES_PATH)

    print("Modelo entrenado correctamente.")
    print(f"Modelo guardado en: {MODEL_PATH}")
    print(f"Respuestas guardadas en: {RESPONSES_PATH}")
    print(f"Exactitud de validación: {accuracy_score(y_test, predictions):.3f}")
    print("\nReporte de clasificación:\n")
    print(classification_report(y_test, predictions, zero_division=0))


if __name__ == "__main__":
    train()
