const boto = document.getElementById("boton");
const botow = document.getElementById("bot");
const cont = document.getElementById("container"); 
const tex = document.getElementById("text");
const sal = document.getElementsByClassName("linkl"); 
let t = true;

boto.addEventListener("click", function() {
    if (t) {
        document.body.style.backgroundColor = "#ffffff";
        cont.style.backgroundColor = "black";
        tex.style.color = "white";  
        boto.style.transform = "translateX(36px)";  

        const links = document.querySelectorAll("a");
        links.forEach(link => {
            link.style.color = "black";
        });

        const items = document.querySelectorAll("i");
        items.forEach(item => {
            item.style.color = "black";
        });

        const spans = document.querySelectorAll("span");
        spans.forEach(span => {
            span.style.color = "black";
        });
    } else {
        document.body.style.backgroundColor = "hsl(0, 0%, 10%)";
        cont.style.backgroundColor = "white";
        tex.style.color = "black";  
        boto.style.transform = "translateX(0px)";  

        const links = document.querySelectorAll("a");
        links.forEach(link => {
            link.style.color = "white";
        });

        const items = document.querySelectorAll("i");
        items.forEach(item => {
            item.style.color = "white";
        });

        const spans = document.querySelectorAll("span");
        spans.forEach(span => {
            span.style.color = "white";
        });
    }
    Array.from(sal).forEach(link => {
        link.style.color = "#E02A19";
    });
    t = !t;
});

document.getElementById("contador").addEventListener("click", async function () {
    try {
        const response = await fetch('/contador/', {
            method: 'POST',
        });
        const result = await response.json();
        if (response.ok) {
            document.getElementById("horasActuales").textContent = result.horasTotales;
            Swal.fire({
                icon: result.status === "success" ? 'success' : 'success',
                title: result.message,
                timer: 3000,
                showConfirmButton: false
            });
        } else {
            document.getElementById("horasActuales").textContent = result.horasTotales;
            Swal.fire({
                icon: result.status === "warning" ? 'warning' : 'error',
                title: result.error,
                timer: 3000,
                showConfirmButton: false
            });
        }
    } catch (error) {
        document.getElementById("horasActuales").textContent = result.horasTotales;
        Swal.fire({
            icon: 'error',
            title: 'Error de conexión. Intenta más tarde.',
            timer: 3000,
            showConfirmButton: false
        });
    }
});
    
    Array.from(sal).forEach(link => {
        link.style.color = "#E02A19";
    });

    t = !t;
