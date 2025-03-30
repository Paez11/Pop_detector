async function classifySong(event) {
    event.preventDefault();  // Evita que el formulario se envíe de forma tradicional

    const formData = new FormData(document.querySelector('form'));
    const lyrics = formData.get('lyrics');  // Captura la letra de la canción
    // Validar si el campo de texto está vacío
    if (!lyrics || lyrics.trim() === "") {
        alert("Por favor, ingresa la letra de una canción antes de clasificar.");
        return;  // Detener la ejecución si no hay letra
    }

    console.log('Lyrics:', lyrics);  // Verifica si la letra se captura correctamente

    // Realiza la solicitud POST a /classify con los datos del formulario
    const response = await fetch('/classify', {
        method: 'POST',
        body: formData
    });

    // Obtiene la respuesta en formato JSON
    const result = await response.json();

    // Si la respuesta es correcta
    if (response.ok) {
        // Muestra la contenedor de resultados
        const resultContainerLogistic = document.querySelector('.resultContainer[data-model="Regresión Logística"]');
        const resultContainerSgd = document.querySelector('.resultContainer[data-model="SGDClassifier"]');
        const resultContainerNN = document.querySelector('.resultContainer[data-model="Red Neuronal"]');

        // Mostrar resultados de Regresión Logística si existe
        if (result['Regresión Logística']) {
            resultContainerLogistic.style.display = 'block';
            const resultTextLogistic = resultContainerLogistic.querySelector('.result-text');
            resultTextLogistic.innerText = result['Regresión Logística'];

            // Cambiar el color del borde según el resultado
            resultContainerLogistic.style.borderColor = result['Regresión Logística'] === "pop" ? '#238636' : '#f5f5f5';
        } else {
            resultContainerLogistic.style.display = 'none';
        }

        // Mostrar resultados de SGDClassifier si existe
        if (result['SGDClassifier']) {
            resultContainerSgd.style.display = 'block';
            const resultTextSgd = resultContainerSgd.querySelector('.result-text');
            resultTextSgd.innerText = result['SGDClassifier'];

            // Cambiar el color del borde según el resultado
            resultContainerSgd.style.borderColor = result['SGDClassifier'] === "pop" ? '#238636' : '#f5f5f5';
        } else {
            resultContainerSgd.style.display = 'none';
        }

        // Mostrar resultados de Red Neuronal si existe
        if (result['Red Neuronal']) {
            resultContainerNN.style.display = 'block';
            const resultTextNN = resultContainerNN.querySelector('.result-text');
            resultTextNN.innerText = result['Red Neuronal'];

            // Cambiar el color del borde según el resultado
            resultContainerNN.style.borderColor = result['Red Neuronal'] === "pop" ? '#238636' : '#f5f5f5';
        } else {
            resultContainerNN.style.display = 'none';
        }
    } else {
        // Si la respuesta es un error, muestra el mensaje
        console.error('Error:', result.error);
        alert('Hubo un error al procesar la solicitud: ' + result.error);
    }
}

function clearForm() {
    // Limpiar el área de texto
    document.querySelector('textarea[name="lyrics"]').value = '';

    // Ocultar los contenedores de resultados
    const resultContainers = document.querySelectorAll('.resultContainer');
    resultContainers.forEach(container => {
        container.style.display = 'none';
    });
}

async function uploadAudio() {
    const audioFile = document.getElementById('audioFile').files[0];
    
    const formData = new FormData(document.querySelector('form'));
    formData.append('audio', audioFile);

    try {
        // Realiza la solicitud POST a /upload con el archivo de audio
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        // Verifica si la respuesta es correcta antes de intentar parsear el JSON
        if (!response.ok) {
            const errorText = await response.text(); // Intenta obtener el texto del error
            throw new Error(`Error en la solicitud: ${errorText}`);
        }

        const result = await response.json();

        // Inserta la letra transcrita en el campo de texto del formulario
        const lyricsTextarea = document.querySelector('textarea[name="lyrics"]');
        if (lyricsTextarea.value.trim() !== "") {
            lyricsTextarea.value += "\n\n" + result.letra;
        } else {
            lyricsTextarea.value = result.letra;
        }
        alert("La transcripción del audio se ha completado y se ha insertado en el formulario.");
    } catch (error) {
        // Manejo de errores
        console.error('Error:', error.message);
        alert('Hubo un error al procesar el archivo de audio: ' + error.message);
    }
}