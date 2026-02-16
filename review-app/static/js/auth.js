// Authentication Form Validation and Enhancement

document.addEventListener('DOMContentLoaded', () => {
    // Password Strength Indicator
    const passwordInput = document.getElementById('password');
    const strengthIndicator = document.getElementById('passwordStrength');

    if (passwordInput && strengthIndicator) {
        passwordInput.addEventListener('input', () => {
            const password = passwordInput.value;
            const strength = calculatePasswordStrength(password);

            strengthIndicator.className = 'password-strength';

            if (password.length === 0) {
                strengthIndicator.className = 'password-strength';
                return;
            }

            if (strength < 3) {
                strengthIndicator.classList.add('weak');
                strengthIndicator.title = 'Weak password';
            } else if (strength < 5) {
                strengthIndicator.classList.add('medium');
                strengthIndicator.title = 'Medium strength password';
            } else {
                strengthIndicator.classList.add('strong');
                strengthIndicator.title = 'Strong password';
            }
        });
    }

    // Password Confirmation Validation
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;

            if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match!');
                return false;
            }
        });
    }
});

// Calculate password strength
function calculatePasswordStrength(password) {
    let strength = 0;

    // Length
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;

    // Lowercase
    if (/[a-z]/.test(password)) strength++;

    // Uppercase
    if (/[A-Z]/.test(password)) strength++;

    // Numbers
    if (/\d/.test(password)) strength++;

    // Special characters
    if (/[^a-zA-Z0-9]/.test(password)) strength++;

    return strength;
}
