// Login Page JavaScript - Long Châu Pharmacy

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive features
    initPasswordToggle();
    initFormValidation();
    initFormFocus();
    initRememberMe();
    initFormSubmission();
});

// Password visibility toggle
function initPasswordToggle() {
    const passwordInput = document.getElementById('password');
    const toggleButton = document.querySelector('.password-toggle');
    
    if (passwordInput && toggleButton) {
        toggleButton.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Update icon
            const icon = this.querySelector('i');
            if (type === 'text') {
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
                this.setAttribute('aria-label', 'Hide password');
            } else {
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
                this.setAttribute('aria-label', 'Show password');
            }
        });
    }
}

// Form focus states
function initFormFocus() {
    const formGroups = document.querySelectorAll('.form-group');
    
    formGroups.forEach(group => {
        const input = group.querySelector('input');
        if (input) {
            input.addEventListener('focus', function() {
                group.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (!this.value.trim()) {
                    group.classList.remove('focused');
                }
            });
            
            // Check if input has value on load
            if (input.value.trim()) {
                group.classList.add('focused');
            }
        }
    });
}

// Form validation
function initFormValidation() {
    const form = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    if (form && usernameInput && passwordInput) {
        // Real-time validation
        usernameInput.addEventListener('input', function() {
            validateField(this, 'Username is required');
        });
        
        passwordInput.addEventListener('input', function() {
            validateField(this, 'Password is required');
        });
        
        // Validate on blur
        usernameInput.addEventListener('blur', function() {
            validateField(this, 'Username is required');
        });
        
        passwordInput.addEventListener('blur', function() {
            validateField(this, 'Password is required');
        });
    }
}

// Field validation helper
function validateField(field, errorMessage) {
    const formGroup = field.closest('.form-group');
    const existingError = formGroup.querySelector('.field-error');
    
    // Remove existing error
    if (existingError) {
        existingError.remove();
    }
    
    // Reset field styles
    field.style.borderColor = '';
    
    // Validate
    if (!field.value.trim()) {
        // Add error
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${errorMessage}`;
        formGroup.appendChild(errorDiv);
        
        // Style field
        field.style.borderColor = '#c33';
        return false;
    }
    
    return true;
}

// Remember me functionality
function initRememberMe() {
    const rememberCheckbox = document.getElementById('remember');
    const rememberLabel = document.querySelector('.remember-me');
    
    if (rememberCheckbox && rememberLabel) {
        rememberLabel.addEventListener('click', function(e) {
            if (e.target !== rememberCheckbox) {
                e.preventDefault();
                rememberCheckbox.checked = !rememberCheckbox.checked;
            }
        });
        
        // Load saved username if remember me was checked
        if (localStorage.getItem('rememberMe') === 'true') {
            const savedUsername = localStorage.getItem('savedUsername');
            if (savedUsername) {
                const usernameInput = document.getElementById('username');
                if (usernameInput) {
                    usernameInput.value = savedUsername;
                    usernameInput.closest('.form-group').classList.add('focused');
                }
                rememberCheckbox.checked = true;
            }
        }
    }
}

// Form submission handling
function initFormSubmission() {
    const form = document.getElementById('loginForm');
    const submitButton = document.querySelector('.login-btn');
    
    if (form && submitButton) {
        form.addEventListener('submit', function(e) {
            // Validate all fields
            const usernameInput = document.getElementById('username');
            const passwordInput = document.getElementById('password');
            const rememberCheckbox = document.getElementById('remember');
            
            let isValid = true;
            
            if (usernameInput && !validateField(usernameInput, 'Username is required')) {
                isValid = false;
            }
            
            if (passwordInput && !validateField(passwordInput, 'Password is required')) {
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
                // Focus on first error field
                const firstError = form.querySelector('.field-error');
                if (firstError) {
                    const errorField = firstError.closest('.form-group').querySelector('input');
                    if (errorField) {
                        errorField.focus();
                    }
                }
                return;
            }
            
            // Handle remember me
            if (rememberCheckbox && usernameInput) {
                if (rememberCheckbox.checked) {
                    localStorage.setItem('rememberMe', 'true');
                    localStorage.setItem('savedUsername', usernameInput.value);
                } else {
                    localStorage.removeItem('rememberMe');
                    localStorage.removeItem('savedUsername');
                }
            }
            
            // Show loading state
            showLoadingState(submitButton);
        });
    }
}

// Show loading state on button
function showLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...';
    button.disabled = true;
    
    // Reset after 10 seconds (fallback)
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    }, 10000);
}

// Utility function to show error messages
function showErrorMessage(message) {
    // Remove existing error messages
    const existingErrors = document.querySelectorAll('.error-message');
    existingErrors.forEach(error => error.remove());
    
    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
    
    // Insert before form
    const form = document.getElementById('loginForm');
    if (form) {
        form.parentNode.insertBefore(errorDiv, form);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }
}

// Keyboard navigation improvements
document.addEventListener('keydown', function(e) {
    // Enter key on remember me label
    if (e.key === 'Enter' && e.target.classList.contains('remember-me')) {
        const checkbox = e.target.querySelector('input[type="checkbox"]');
        if (checkbox) {
            checkbox.checked = !checkbox.checked;
        }
    }
    
    // Escape key to clear errors
    if (e.key === 'Escape') {
        const errors = document.querySelectorAll('.error-message, .field-error');
        errors.forEach(error => error.remove());
        
        // Reset field styles
        const fields = document.querySelectorAll('input[type="text"], input[type="password"]');
        fields.forEach(field => {
            field.style.borderColor = '';
        });
    }
});

// Accessibility improvements
function enhanceAccessibility() {
    // Add ARIA labels
    const passwordToggle = document.querySelector('.password-toggle');
    if (passwordToggle) {
        passwordToggle.setAttribute('aria-label', 'Show password');
        passwordToggle.setAttribute('tabindex', '0');
    }
    
    // Add form labels association
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    if (usernameInput) {
        usernameInput.setAttribute('aria-describedby', 'username-help');
    }
    
    if (passwordInput) {
        passwordInput.setAttribute('aria-describedby', 'password-help');
    }
}

// Initialize accessibility features
document.addEventListener('DOMContentLoaded', enhanceAccessibility);

// Handle form errors from server
window.addEventListener('load', function() {
    // Check for Django form errors
    const djangoErrors = document.querySelectorAll('.errorlist');
    if (djangoErrors.length > 0) {
        djangoErrors.forEach(errorList => {
            const errors = errorList.querySelectorAll('li');
            errors.forEach(error => {
                showErrorMessage(error.textContent);
            });
        });
    }
});