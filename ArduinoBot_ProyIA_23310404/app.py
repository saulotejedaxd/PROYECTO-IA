"""
Aplicación web de ArduinoBot.
Ejecutar con: python app.py
"""
from flask import Flask, jsonify, render_template, request

from src.chatbot import ArduinoBot

app = Flask(__name__)
bot = ArduinoBot()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    result = bot.answer(message)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
