import pickle
from tensorflow import keras  # Para cargar el modelo de red neuronal
import numpy as np
from flask import Flask, render_template, request, jsonify

# Cargamos los modelos
with open('models/tfidf_model.pkl', 'rb') as f:
    model_tfidf = pickle.load(f)

with open('models/logistic_regression_model_1.1a.pkl', 'rb') as f:
    modelo_logistico = pickle.load(f)

with open('models/sgd_classifier_model_1.1a.pkl', 'rb') as f:
    modelo_sgd = pickle.load(f)

modelo_nn = keras.models.load_model('models/pop_detected_network_1.1a.h5')

def classify_song(lyrics: str) -> dict:
    """
    Clasifica la canción con los tres modelos.
    
    :param lyrics: Letra de la canción en formato string.
    :return: Diccionario con los resultados de cada modelo.
    """
    # Vectorizar la letra de la canción usando el TfidfVectorizer
    lyrics_vectorized = model_tfidf.transform([lyrics])

    # Clasificación con cada modelo
    resultado_sgd = modelo_sgd.predict(lyrics_vectorized)[0]
    resultado_nn = modelo_nn.predict(lyrics_vectorized.toarray())[0][0]  # Convertir a float
    resultado_logistico = modelo_logistico.predict(lyrics_vectorized.toarray())[0]

    # Convertir los resultados a tipos nativos de Python
    resultado_nn = "Pop" if resultado_nn >= 0.5 else "Non-pop"  # Convertir a string
    resultado_sgd = str(resultado_sgd)  # Convertir a string
    resultado_logistico = str(resultado_logistico)  # Convertir a string

    return {
        'SGDClassifier': resultado_sgd,
        'Red Neuronal': resultado_nn,
        'Regresión Logística': resultado_logistico
    }

app = Flask(__name__)