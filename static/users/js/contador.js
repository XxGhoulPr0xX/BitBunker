let startTime = null;
let accumulatedTime = 12 * 3600; 
let intervalId = null;
const totalHoursGoal = 500 * 3600; 
const endHour = 19;
const startHour = 9;

function updateTime() {
    const currentTime = new Date();
    if (currentTime.getHours() >= startHour && currentTime.getHours() < endHour) {
        const elapsedTime = Math.floor((Date.now() - startTime) / 1000) + accumulatedTime;
        const hours = Math.floor(elapsedTime / 3600);
        const minutes = Math.floor((elapsedTime % 3600) / 60);
        const seconds = elapsedTime % 60;

        if (elapsedTime >= totalHoursGoal) {
            clearInterval(intervalId);
            document.getElementById('elapsed-time').textContent = '500 horas completadas';
        } else {
            document.getElementById('elapsed-time').textContent = `${hours} horas ${minutes} minutos ${seconds} segundos`;
        }
    } else {
        clearInterval(intervalId);
        document.getElementById('elapsed-time').textContent = 'El cronómetro se detuvo (fuera del horario permitido)';
    }
}

document.querySelector('.button').addEventListener('click', function () {
    const currentTime = new Date();
    if (currentTime.getHours() >= startHour && currentTime.getHours() < endHour) {
        if (!intervalId) {
            startTime = Date.now();
            intervalId = setInterval(updateTime, 1000);
        }
    } else {
        document.getElementById('elapsed-time').textContent = 'El cronómetro solo puede iniciarse entre las 9 AM y las 7 PM.';
    }
});


setInterval(function () {
    const currentTime = new Date();
    if (currentTime.getHours() >= endHour && intervalId) {
        clearInterval(intervalId);
        intervalId = null;
        document.getElementById('elapsed-time').textContent = 'El cronómetro se ha apagado automáticamente a las 7 PM.';
    }
}, 1000);
