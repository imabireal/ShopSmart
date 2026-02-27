class Chatbot {
    constructor() {
        this.chatContainer = null;
        this.chatMessages = null;
        this.messageInput = null;
        this.sendButton = null;
        this.clearButton = null;
        this.toggleButton = null;
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        this.createChatInterface();
        this.bindEvents();
        this.loadChatHistory();
    }
    
    createChatInterface() {
        // Create chat container
        this.chatContainer = document.createElement('div');
        this.chatContainer.id = 'chatbot-container';
        this.chatContainer.className = 'chatbot-container';
        
        // Create chat header
        const chatHeader = document.createElement('div');
        chatHeader.className = 'chatbot-header';
        chatHeader.innerHTML = `
            <div class="chatbot-title">
                <i class="fas fa-robot"></i>
                ShopSmart Assistant
            </div>
            <button id="chatbot-close" class="chatbot-close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        // Create chat messages container
        this.chatMessages = document.createElement('div');
        this.chatMessages.className = 'chatbot-messages';
        
        // Create chat input container
        const chatInput = document.createElement('div');
        chatInput.className = 'chatbot-input';
        
        this.messageInput = document.createElement('input');
        this.messageInput.type = 'text';
        this.messageInput.id = 'chatbot-message';
        this.messageInput.placeholder = 'Type your message...';
        this.messageInput.className = 'chatbot-input-field';
        
        this.sendButton = document.createElement('button');
        this.sendButton.id = 'chatbot-send';
        this.sendButton.className = 'chatbot-send';
        this.sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        
        this.clearButton = document.createElement('button');
        this.clearButton.id = 'chatbot-clear';
        this.clearButton.className = 'chatbot-clear';
        this.clearButton.innerHTML = '<i class="fas fa-trash"></i>';
        
        chatInput.appendChild(this.messageInput);
        chatInput.appendChild(this.sendButton);
        chatInput.appendChild(this.clearButton);
        
        // Create chat toggle button
        this.toggleButton = document.createElement('button');
        this.toggleButton.id = 'chatbot-toggle';
        this.toggleButton.className = 'chatbot-toggle';
        this.toggleButton.innerHTML = '<i class="fas fa-comments"></i>';
        
        // Assemble chat container
        this.chatContainer.appendChild(chatHeader);
        this.chatContainer.appendChild(this.chatMessages);
        this.chatContainer.appendChild(chatInput);
        
        // Append to body
        document.body.appendChild(this.chatContainer);
        document.body.appendChild(this.toggleButton);
        
        // Hide chat container initially
        this.chatContainer.style.display = 'none';
    }
    
    bindEvents() {
        // Toggle chat window
        this.toggleButton.addEventListener('click', () => this.toggleChat());
        document.getElementById('chatbot-close').addEventListener('click', () => this.toggleChat());
        
        // Send message
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Clear chat
        this.clearButton.addEventListener('click', () => this.clearChat());
    }
    
    toggleChat() {
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            this.chatContainer.style.display = 'flex';
            this.toggleButton.classList.add('active');
            setTimeout(() => {
                this.chatContainer.classList.add('open');
            }, 10);
        } else {
            this.chatContainer.classList.remove('open');
            this.toggleButton.classList.remove('active');
            setTimeout(() => {
                this.chatContainer.style.display = 'none';
            }, 300);
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            return;
        }
        
        // Add user message to chat
        this.addMessage('user', message);
        
        // Clear input
        this.messageInput.value = '';
        
        // Show typing indicator
        const typingIndicator = this.addTypingIndicator();
        
        try {
            // Send message to server
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            typingIndicator.remove();
            
            if (data.error) {
                this.addMessage('bot', `Error: ${data.error}`);
            } else {
                // Add bot response
                this.addMessage('bot', data.response);
                
                // Add product recommendations if available
                if (data.recommendations && data.recommendations.length > 0) {
                    this.addRecommendations(data.recommendations);
                }
            }
        } catch (error) {
            // Remove typing indicator
            typingIndicator.remove();
            
            this.addMessage('bot', 'Sorry, there was an error processing your request. Please try again later.');
            console.error('Chatbot error:', error);
        }
    }
    
    addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'chatbot-message-content';
        messageContent.textContent = text;
        
        const messageAvatar = document.createElement('div');
        messageAvatar.className = 'chatbot-message-avatar';
        messageAvatar.innerHTML = sender === 'user' 
            ? '<i class="fas fa-user"></i>' 
            : '<i class="fas fa-robot"></i>';
        
        if (sender === 'user') {
            messageDiv.appendChild(messageContent);
            messageDiv.appendChild(messageAvatar);
        } else {
            messageDiv.appendChild(messageAvatar);
            messageDiv.appendChild(messageContent);
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chatbot-message bot-message';
        
        const avatar = document.createElement('div');
        avatar.className = 'chatbot-message-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.innerHTML = `
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        typingDiv.appendChild(avatar);
        typingDiv.appendChild(typingIndicator);
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
        
        return typingDiv;
    }
    
    addRecommendations(recommendations) {
        const recommendationsDiv = document.createElement('div');
        recommendationsDiv.className = 'chatbot-recommendations';
        
        const title = document.createElement('div');
        title.className = 'chatbot-recommendations-title';
        title.textContent = 'Recommended Products:';
        
        const productsContainer = document.createElement('div');
        productsContainer.className = 'chatbot-products-container';
        
        recommendations.forEach(product => {
            const productDiv = document.createElement('div');
            productDiv.className = 'chatbot-product';
            productDiv.innerHTML = `
                <div class="chatbot-product-image">
                    <img src="${product.image_url || '/static/images/no-image.png'}" alt="${product.title}">
                </div>
                <div class="chatbot-product-info">
                    <div class="chatbot-product-title">${this.truncateText(product.title, 30)}</div>
                    <div class="chatbot-product-brand">${product.brand}</div>
                    <div class="chatbot-product-category">${product.category}</div>
                    <div class="chatbot-product-price">₹${product.price.toLocaleString()}</div>
                </div>
            `;
            
            productDiv.addEventListener('click', () => this.openProduct(product.id));
            
            productsContainer.appendChild(productDiv);
        });
        
        recommendationsDiv.appendChild(title);
        recommendationsDiv.appendChild(productsContainer);
        
        const botMessage = document.createElement('div');
        botMessage.className = 'chatbot-message bot-message chatbot-recommendations-message';
        botMessage.appendChild(recommendationsDiv);
        
        this.chatMessages.appendChild(botMessage);
        this.scrollToBottom();
    }
    
    openProduct(productId) {
        // Open product detail page
        window.location.href = `/product/${productId}`;
    }
    
    truncateText(text, maxLength) {
        if (text.length <= maxLength) {
            return text;
        }
        
        return text.substring(0, maxLength - 3) + '...';
    }
    
    async clearChat() {
        try {
            await fetch('/chat/clear', {
                method: 'POST'
            });
            
            this.chatMessages.innerHTML = '';
            this.loadChatHistory();
        } catch (error) {
            console.error('Error clearing chat:', error);
            this.chatMessages.innerHTML = '';
        }
    }
    
    loadChatHistory() {
        // Add welcome message
        this.addMessage('bot', "Hello! I'm ShopSmart assistant. I can help you find products, recommend items based on your needs, and answer questions about our products. How can I assist you today?");
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Chatbot();
});
