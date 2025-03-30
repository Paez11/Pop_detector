import os
import speech_recognition as sr
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta donde se guardarán los audios

# Asegurarse de que la carpeta de uploads existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def transcribe_audio(audio_path):
    if not os.path.exists(audio_path):
        return "El archivo de audio no existe. Por favor, verifica la ruta y vuelve a intentarlo."

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        try:
            # Cambiar el código de idioma a uno válido
            text = recognizer.recognize_google(audio_data, language="en-US")
            print("Texto transcrito:", text)  # Depuración
            return text
        except sr.UnknownValueError:
            return "No se pudo reconocer el audio. Por favor, intenta con un archivo más claro."
        except sr.RequestError as e:
            return f"Error con el servicio de reconocimiento de voz: {e}"
    except (FileNotFoundError, ValueError) as e:
        return f"Error al procesar el archivo de audio: {e}"
    