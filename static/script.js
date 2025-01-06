document.addEventListener("DOMContentLoaded", function() {
    const timerElement = document.getElementById("timer");
    let timeLeft = 180; // 3分

    const updateTimer = () => {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes}:${seconds < 10 ? "0" + seconds : seconds}`;
        if (timeLeft <= 0) {
            alert("時間切れです！");
            document.getElementById("user-input-form").submit();
        }
        timeLeft--;
    };

    setInterval(updateTimer, 1000);
});



