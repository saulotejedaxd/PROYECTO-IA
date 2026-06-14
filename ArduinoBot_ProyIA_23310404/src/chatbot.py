"""
ArduinoBot - Motor de conversación.
Clasifica el mensaje del usuario y responde con una recomendación técnica.
"""
from __future__ import annotations

import random
import re
import math
from pathlib import Path
from typing import Dict, Any

import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "arduino_intent_model.joblib"
RESPONSES_PATH = BASE_DIR / "models" / "responses.joblib"


class ArduinoBot:
    """Chatbot educativo para diagnóstico de fallas comunes en Arduino."""

    def __init__(self, confidence_threshold: float = 0.08) -> None:
        if not MODEL_PATH.exists() or not RESPONSES_PATH.exists():
            raise FileNotFoundError(
                "No se encontró el modelo entrenado. Ejecuta primero: python src/train_model.py"
            )

        self.model = joblib.load(MODEL_PATH)
        self.responses = joblib.load(RESPONSES_PATH)
        self.confidence_threshold = confidence_threshold

    def answer(self, message: str) -> Dict[str, Any]:
        """Devuelve intención, confianza y respuesta."""
        clean_message = message.strip()
        if not clean_message:
            return {
                "intent": "fallback",
                "confidence": 0.0,
                "response": "Escribe una falla. Ejemplo: mi LED no prende o no puedo subir código.",
                "extra": ""
            }

        intent = str(self.model.predict([clean_message])[0])
        confidence = self._estimate_confidence(clean_message, intent)

        if confidence < self.confidence_threshold:
            intent = "fallback"

        response = random.choice(self.responses.get(intent, self.responses["fallback"]))
        extra = self._extract_extra_hint(clean_message, intent)

        return {
            "intent": intent,
            "confidence": round(confidence, 3),
            "response": response,
            "extra": extra,
        }


    def _estimate_confidence(self, message: str, intent: str) -> float:
        """Estima una confianza sencilla desde los puntajes del clasificador SVM."""
        try:
            scores = self.model.decision_function([message])[0]
            classes = list(self.model.classes_)
            max_score = max(scores)
            exp_scores = [math.exp(score - max_score) for score in scores]
            total = sum(exp_scores)
            index = classes.index(intent)
            return float(exp_scores[index] / total) if total else 0.0
        except Exception:
            return 0.0

    @staticmethod
    def _extract_extra_hint(message: str, intent: str) -> str:
        """Agrega una pista contextual si detecta datos útiles en el mensaje."""
        lowered = message.lower()
        pins = re.findall(r"(?:pin|pines?)\s*(\d+)", lowered)
        volts = re.findall(r"(\d+(?:\.\d+)?)\s*v", lowered)

        hints = []
        if pins:
            hints.append(f"Detecté que mencionas el pin {', '.join(pins)}; confirma que coincide con el código.")
        if volts:
            hints.append(f"Detecté una alimentación de {', '.join(volts)} V; revisa que sea compatible con el módulo.")
        if "motor" in lowered and intent != "motor_dc_no_gira":
            hints.append("Si hay motor involucrado, no lo alimentes directo desde un pin de Arduino.")
        if "rele" in lowered or "relay" in lowered:
            hints.append("Precaución: si controlas corriente alterna, desconecta la energía antes de modificar cableado.")

        return " ".join(hints)
