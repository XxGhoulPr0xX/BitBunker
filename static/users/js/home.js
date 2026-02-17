document.getElementById("contador").addEventListener("click", async function () {
    try {
        const response = await fetch('/contador/', {
            method: 'POST',
        });
        const result = await response.json();
        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true
        });
        if (response.ok) {
            document.getElementById("horasActuales").textContent = result.horasTotales;
            Toast.fire({
                icon: 'success',
                title: result.message
            });
        } else {
            Toast.fire({
                icon: 'warning',
                title: result.error || 'Ya registraste hoy'
            });
        }
    } catch (error) {
        console.error('Error:', error);
    }
});