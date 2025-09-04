/**
 * Real-time password validation and strength indicator
 */
document.addEventListener('DOMContentLoaded', function() {
    const passwordInputs = document.querySelectorAll('input[type="password"][name="password1"]');
    
    passwordInputs.forEach(function(input) {
        // Create strength indicator
        const strengthIndicator = document.createElement('div');
        strengthIndicator.className = 'password-strength mt-2';
        strengthIndicator.innerHTML = `
            <div class="progress" style="height: 5px;">
                <div class="progress-bar" role="progressbar" style="width: 0%"></div>
            </div>
            <small class="strength-text text-muted mt-1"></small>
        `;
        
        // Insert after the input field
        input.parentNode.insertBefore(strengthIndicator, input.nextSibling);
        
        const progressBar = strengthIndicator.querySelector('.progress-bar');
        const strengthText = strengthIndicator.querySelector('.strength-text');
        
        // Real-time validation
        input.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            
            // Update progress bar
            progressBar.style.width = strength.score + '%';
            progressBar.className = 'progress-bar ' + strength.class;
            
            // Update strength text
            strengthText.textContent = strength.text;
            strengthText.className = 'strength-text mt-1 ' + strength.textClass;
            
            // Show/hide requirements
            updateRequirements(password);
        });
    });
    
    function calculatePasswordStrength(password) {
        let score = 0;
        let requirements = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            lowercase: /[a-z]/.test(password),
            number: /\d/.test(password),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };
        
        // Calculate score
        Object.values(requirements).forEach(met => {
            if (met) score += 20;
        });
        
        // Determine strength level
        if (score < 40) {
            return {
                score: score,
                class: 'bg-danger',
                text: 'Very Weak',
                textClass: 'text-danger'
            };
        } else if (score < 60) {
            return {
                score: score,
                class: 'bg-warning',
                text: 'Weak',
                textClass: 'text-warning'
            };
        } else if (score < 80) {
            return {
                score: score,
                class: 'bg-info',
                text: 'Good',
                textClass: 'text-info'
            };
        } else {
            return {
                score: score,
                class: 'bg-success',
                text: 'Strong',
                textClass: 'text-success'
            };
        }
    }
    
    function updateRequirements(password) {
        const requirements = document.querySelectorAll('.password-requirement');
        requirements.forEach(function(req) {
            const type = req.dataset.requirement;
            let met = false;
            
            switch(type) {
                case 'length':
                    met = password.length >= 8;
                    break;
                case 'uppercase':
                    met = /[A-Z]/.test(password);
                    break;
                case 'lowercase':
                    met = /[a-z]/.test(password);
                    break;
                case 'number':
                    met = /\d/.test(password);
                    break;
                case 'special':
                    met = /[!@#$%^&*(),.?":{}|<>]/.test(password);
                    break;
            }
            
            req.className = 'password-requirement ' + (met ? 'text-success' : 'text-muted');
            req.innerHTML = (met ? '✓ ' : '○ ') + req.textContent.replace(/^[✓○] /, '');
        });
    }
});
