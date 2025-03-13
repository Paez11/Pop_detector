import pickle
from tensorflow import keras  # Para cargar el modelo de red neuronal
import numpy as np

# Cargamos los modelos
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
    lyrics_vector = [lyrics]  # Lista con la letra para Regresión Logística y SGDClassifier
    lyrics_array = np.array(lyrics_vector).reshape(-1, 1)  # Aseguramos que sea 2D para la Red Neuronal

    # Clasificación con cada modelo
    resultado_logistico = modelo_logistico.predict(lyrics_array)[0]  # Aseguramos que se pase un array 2D
    resultado_sgd = modelo_sgd.predict(lyrics_array)[0]  # Aseguramos que se pase un array 2D
    resultado_nn = modelo_nn.predict(lyrics_array)
    resultado_nn = "Pop" if resultado_nn >= 0.5 else "No Pop"  # Ajustamos la clasificación para la Red Neuronal

    return {
        'Regresión Logística': resultado_logistico,
        'SGDClassifier': resultado_sgd,
        'Red Neuronal': resultado_nn
    }
