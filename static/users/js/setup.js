function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

async function sendDataToServer(reportNumber) {
    const data = {
        reportNumber: reportNumber,
        firstName: document.getElementById('firstName').value || 'Nombre',
        middleName: document.getElementById('middleName').value || 'Apellido Paterno',
        lastName: document.getElementById('lastName').value || 'Apellido Materno',
        semester: document.getElementById('semester').value || 'Semestre',
    };
    try {
        const response = await fetch('/save_pdf/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify(data),
        });
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Reporte_${reportNumber}.pdf`; // Nombre del archivo al descargar
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } else {
            alert('Error al generar el PDF.');
        }
    } catch (error) {
        console.error('Error al enviar los datos al servidor:', error);
        alert('Error al conectar con el servidor.');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('q').addEventListener('click', () => sendDataToServer(1));
    document.getElementById('w').addEventListener('click', () => sendDataToServer(2));
    document.getElementById('e').addEventListener('click', () => sendDataToServer(3));
});