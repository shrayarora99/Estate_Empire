// Estate Empire Lite - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Credit score slider
    const creditScoreSlider = document.getElementById('credit-score-slider');
    const creditScoreValue = document.getElementById('credit-score-value');
    
    if (creditScoreSlider && creditScoreValue) {
        creditScoreSlider.addEventListener('input', function() {
            creditScoreValue.textContent = this.value;
        });
    }
    
    // Income formatter
    const incomeInput = document.getElementById('annual-income');
    
    if (incomeInput) {
        incomeInput.addEventListener('input', function(e) {
            // Remove non-numeric characters
            let value = this.value.replace(/\D/g, '');
            
            // Format with commas
            if (value) {
                value = parseInt(value, 10).toLocaleString('en-US');
            }
            
            this.value = value;
        });
    }
    
    // Simple mock chatbot - Very basic implementation
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-message');
    
    if (chatbotToggle && chatbotContainer) {
        chatbotToggle.addEventListener('click', function() {
            chatbotContainer.classList.toggle('d-none');
            
            // Add initial message if chat is empty
            if (chatMessages && chatMessages.children.length === 0) {
                addBotMessage("Hi there! I'm your Estate Empire assistant. How can I help you find your perfect rental?");
            }
        });
    }
    
    if (sendButton && chatInput && chatMessages) {
        sendButton.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            // Add user message
            addUserMessage(message);
            
            // Clear input
            chatInput.value = '';
            
            // Simulate bot thinking
            setTimeout(() => {
                const botResponse = getBotResponse(message.toLowerCase());
                addBotMessage(botResponse);
            }, 500);
        }
    }
    
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message user-message';
        messageElement.innerHTML = `
            <div class="message-content bg-primary text-white p-2 rounded mb-2 ms-auto">
                ${message}
            </div>
        `;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message bot-message';
        messageElement.innerHTML = `
            <div class="message-content bg-light p-2 rounded mb-2 me-auto">
                ${message}
            </div>
        `;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function getBotResponse(message) {
        // Very simple response logic
        if (message.includes('hello') || message.includes('hi') || message.includes('hey')) {
            return "Hello! How can I help you find your perfect rental today?";
        } else if (message.includes('rent') || message.includes('price') || message.includes('cost')) {
            return "Our listings range from $1,800 to $5,800 per month. What's your budget?";
        } else if (message.includes('neighborhood') || message.includes('area') || message.includes('location')) {
            return "We have properties in Chelsea, Williamsburg, Upper East Side, Astoria, Park Slope, and Washington Heights. Do you have a preferred area?";
        } else if (message.includes('credit') || message.includes('score')) {
            return "Most of our landlords require a credit score of at least 650, but some properties accept lower scores with a guarantor.";
        } else if (message.includes('pet') || message.includes('dog') || message.includes('cat')) {
            return "Many of our properties are pet-friendly! You can filter for pet-friendly options in your search.";
        } else if (message.includes('application') || message.includes('apply')) {
            return "To apply, click the 'Get Matched' button and fill out our pre-screening form. We'll match you with properties that fit your needs!";
        } else if (message.includes('thank')) {
            return "You're welcome! Let me know if you need anything else.";
        } else {
            return "I'm not sure I understand. Can you try rephrasing your question? Or you can ask about rent prices, neighborhoods, credit requirements, or how to apply.";
        }
    }
});
