from flask import Flask, render_template, request, jsonify
from Classifier import classify_song 
import os

app = Flask(__name__)

# Asegúrate de que Flask pueda servir archivos estáticos
#app.static_folder = 'templates/static'

home = "index.html"

# Ruta principal para mostrar el formulario
@app.route('/')
def index():
    return render_template(home)

# Ruta para procesar la canción enviada desde el formulario
@app.route('/classify', methods=['POST'])
def classify():
    try:
        if request.method == 'POST':
            song_lyrics = request.form.get('lyrics')  # Usar get para evitar KeyError
            if not song_lyrics:
                return jsonify({"error": "No lyrics provided"}), 400  # Error si no se envían letras
            
            # Llamar al modelo de clasificación para obtener resultados de todos los modelos
            resultados = classify_song(song_lyrics)
            
            return jsonify(resultados)
    except Exception as e:
        # Capturar excepciones y devolver un mensaje de error con detalles
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
