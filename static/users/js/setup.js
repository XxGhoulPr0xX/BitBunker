document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('q').addEventListener('click', function () {
        sendDataToServer(1);
    });
    document.getElementById('w').addEventListener('click', function () {
        sendDataToServer(2);
    });
    document.getElementById('e').addEventListener('click', function () {
        sendDataToServer(3);
    });
});

async function sendDataToServer(reportNumber) {
    const data = {
        reportNumber: reportNumber,
        firstName: document.getElementById('firstName').value || 'Nombre',
        middleName: document.getElementById('middleName').value || 'Apellido Paterno',
        lastName: document.getElementById('lastName').value || 'Apellido Materno',
        semester: document.getElementById('semester').value || 'Semestre',
    };

    try {
        const response = await fetch(urls.content, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            alert('PDF generado y guardado.');
        } else {
            alert('Error al generar el PDF.');
        }
    } catch (error) {
        console.error('Error al enviar los datos al servidor:', error);
        alert('Error al conectar con el servidor.');
    }
}