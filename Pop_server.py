from flask import Flask, render_template, request, jsonify
from Classifier import classify_song 
from AudioRecognizerTS import transcribe_audio
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

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

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No se ha subido ningún archivo.'})

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío.'})

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Guardando archivo en: {file_path}")  # Depuración
    file.save(file_path)

    # Transcribir el audio a texto
    lyrics = transcribe_audio(file_path)

    # Verificar si la transcripción devolvió un error
    if isinstance(lyrics, str) and lyrics.startswith("Error"):
        return jsonify({'error': lyrics}), 400  # Devolver el error como respuesta

    # Clasificar la letra transcrita
    resultados = classify_song(lyrics)

    return jsonify({'letra': lyrics, 'resultados': resultados})

if __name__ == '__main__':
    app.run(debug=True)
