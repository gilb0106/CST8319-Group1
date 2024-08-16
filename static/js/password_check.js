document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.querySelector('form');
    const passwordInput = document.getElementById('password');
    const errorElement = document.createElement('div');
    errorElement.style.color = 'red';

    form.addEventListener('submit', function(event) {
        const password = passwordInput.value;

        // Password validation regex
        const lengthCheck = /.{8,}/;
        const uppercaseCheck = /[A-Z]/;
        const lowercaseCheck = /[a-z]/;
        const numberCheck = /[0-9]/;
        const specialCharacterCheck = /[!@#$%^&*(),.?":{}|<>]/;

        let errorMessage = '';

        if (!lengthCheck.test(password)) {
            errorMessage += 'Password must be at least 8 characters long.<br>';
        }
        if (!uppercaseCheck.test(password)) {
            errorMessage += 'Password must contain at least one uppercase letter.<br>';
        }
        if (!lowercaseCheck.test(password)) {
            errorMessage += 'Password must contain at least one lowercase letter.<br>';
        }
        if (!numberCheck.test(password)) {
            errorMessage += 'Password must contain at least one number.<br>';
        }
        if (!specialCharacterCheck.test(password)) {
            errorMessage += 'Password must contain at least one special character.<br>';
        }

        if (errorMessage) {
            errorElement.innerHTML = errorMessage;
            form.appendChild(errorElement);
            event.preventDefault();
        }
    });
});
