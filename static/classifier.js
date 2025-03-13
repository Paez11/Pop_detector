async function classifySong(event) {
    event.preventDefault();  // Evita que el formulario se envíe de forma tradicional

    const formData = new FormData(document.querySelector('form'));
    const lyrics = formData.get('lyrics');  // Captura la letra de la canción
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

        // Mostrar resultados de Regresión Logística
        resultContainerLogistic.style.display = 'block';
        const resultTextLogistic = resultContainerLogistic.querySelector('.result-text');
        resultTextLogistic.innerText = result['Regresión Logística'];

        // Mostrar resultados de SGDClassifier
        resultContainerSgd.style.display = 'block';
        const resultTextSgd = resultContainerSgd.querySelector('.result-text');
        resultTextSgd.innerText = result['SGDClassifier'];

        // Mostrar resultados de Red Neuronal
        resultContainerNN.style.display = 'block';
        const resultTextNN = resultContainerNN.querySelector('.result-text');
        resultTextNN.innerText = result['Red Neuronal'];

        // Cambiar el color del borde según el resultado de cada modelo
        if (result['Regresión Logística'] === "Pop") {
            resultContainerLogistic.style.borderColor = 'green';
        } else {
            resultContainerLogistic.style.borderColor = 'red';
        }

        if (result['SGDClassifier'] === "Pop") {
            resultContainerSgd.style.borderColor = 'green';
        } else {
            resultContainerSgd.style.borderColor = 'red';
        }

        if (result['Red Neuronal'] === "Pop") {
            resultContainerNN.style.borderColor = 'green';
        } else {
            resultContainerNN.style.borderColor = 'red';
        }
    } else {
        // Si la respuesta es un error, muestra el mensaje
        console.error('Error:', result.error);
        alert('Hubo un error al procesar la solicitud: ' + result.error);
    }
}
