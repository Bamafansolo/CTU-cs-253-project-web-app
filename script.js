document.addEventListener('DOMContentLoaded', function() {
    // Form submission
    const waitlistForm = document.getElementById('waitlistForm');
    const submitButton = document.getElementById('submitButton');
    const submitSpinner = document.getElementById('submitSpinner');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');
    
    if (waitlistForm) {
        waitlistForm.addEventListener('submit', handleFormSubmit);
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 70, // Adjust for fixed header
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Form validation and submission handler
    function handleFormSubmit(e) {
        e.preventDefault();
        
        // Reset form state
        resetFormState();
        
        // Get form values
        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();
        
        // Validate form
        let isValid = true;
        
        if (!fullName || fullName.length < 2) {
            showFieldError('fullName', 'Please enter your full name');
            isValid = false;
        }
        
        if (!isValidEmail(email)) {
            showFieldError('email', 'Please enter a valid email address');
            isValid = false;
        }
        
        if (!isValid) return;
        
        // Show loading state
        setLoadingState(true);
        
        // Send registration data to server
        fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ fullName, email }),
        })
        .then(response => response.json())
        .then(data => {
            setLoadingState(false);
            
            if (data.success) {
                // Show success message
                successMessage.textContent = data.message;
                successMessage.classList.remove('d-none');
                
                // Reset form
                waitlistForm.reset();
                
                // Scroll to success message
                successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                // Show error message
                showFormError(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            setLoadingState(false);
            showFormError('An unexpected error occurred. Please try again later.');
        });
    }
    
    // Helper functions
    function isValidEmail(email) {
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return re.test(email);
    }
    
    function resetFormState() {
        // Hide messages
        successMessage.classList.add('d-none');
        errorMessage.classList.add('d-none');
        
        // Reset field validation
        const fields = ['fullName', 'email'];
        fields.forEach(field => {
            const element = document.getElementById(field);
            element.classList.remove('is-invalid');
        });
    }
    
    function showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        const feedback = document.getElementById(`${fieldId}Feedback`);
        
        field.classList.add('is-invalid');
        if (feedback) {
            feedback.textContent = message;
        }
    }
    
    function showFormError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('d-none');
        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    function setLoadingState(isLoading) {
        if (isLoading) {
            submitButton.disabled = true;
            submitSpinner.classList.remove('d-none');
        } else {
            submitButton.disabled = false;
            submitSpinner.classList.add('d-none');
        }
    }
});
