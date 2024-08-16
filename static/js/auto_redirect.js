function delayedRedirect() {
    var countdownElement = document.getElementById('countdown');
    var seconds = 3; // Initial countdown time in seconds
    // Set the initial countdown text
    if (countdownElement) {
        countdownElement.textContent = seconds;
    }
    var interval = setInterval(function() {
        seconds--;
        if (countdownElement) {
            countdownElement.textContent = seconds;
        }
        if (seconds <= 0) {
            clearInterval(interval);
            window.location.href = "/"; // Redirect to the desired URL
        }
    }, 1000); // Update every second
}