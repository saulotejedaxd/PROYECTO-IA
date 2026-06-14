ArduinoBot - Proyecto IA

Autor: Saulo Tejeda
Registro: 23310404
Proyecto: Chatbot de diagnóstico para fallas comunes en Arduino

Descripción

ArduinoBot es un chatbot hecho en Python que ayuda a diagnosticar fallas comunes en prácticas con Arduino.
El usuario escribe un problema, por ejemplo “mi LED no prende” o “mi servo tiembla”, y el bot responde con una posible causa y una recomendación técnica.

El chatbot fue entrenado con un dataset propio de intenciones relacionadas con errores básicos de Arduino.

Tecnologías usadas
Python
Flask
Scikit-learn
HTML
CSS
GitHub Codespaces
Estructura básica
app.py
requirements.txt
README.md
data/
src/
models/
templates/
static/
Cómo correr el proyecto

Entrar a la carpeta del proyecto:

cd /workspaces/PROYECTO-IA/ArduinoBot_ProyIA_23310404

Instalar dependencias:

pip install -r requirements.txt

Entrenar el modelo:

python src/train_model.py

Ejecutar la aplicación:

python app.py

Después abrir el puerto 5000 desde la pestaña PUERTOS en Codespaces.

Forma rápida de correrlo

Si el modelo ya fue entrenado antes, solo se ejecuta:

cd /workspaces/PROYECTO-IA/ArduinoBot_ProyIA_23310404
python app.py
Ejemplos de uso

Puedes probar preguntas como:

mi led no prende
mi arduino no sube el código
mi sensor ultrasónico marca mal
mi servo tiembla
mi pantalla lcd no muestra texto
mi motor no gira
Funcionamiento
El usuario escribe una falla.
El chatbot analiza el texto.
El modelo clasifica la intención.
El sistema muestra una respuesta con una recomendación.