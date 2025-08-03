/**
 * University Guidance Chatbot - Complete JavaScript Implementation
 * Handles chat functionality, academic guidance, and user interactions
 */

class UniversityGuidanceChatbot {
    constructor() {
        // Chat elements
        this.messageInput = document.getElementById('message-input');
        this.chatMessages = document.getElementById('chat-messages');
        this.sendButton = document.getElementById('send-button');
        this.typingIndicator = document.getElementById('typing-indicator');

        // State management
        this.isProcessing = false;
        this.messageHistory = [];
        this.currentConversationId = null;

        // Configuration
        this.config = {
            maxMessageLength: 500,
            typingDelay: 1000,
            clearInputDelay: 100,
            autoScrollOffset: 100,
            retryAttempts: 3
        };

        this.init();
    }

    /**
     * Initialize the chatbot
     */
    init() {
        this.setupEventListeners();
        this.loadChatHistory();
        this.focusInput();
        this.setupKeyboardShortcuts();
        this.initializeAutoResize();

        // Set initial state
        this.updateSendButtonState();
        this.scrollToBottom();

        console.log('University Guidance Chatbot initialized successfully');
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Send button click
        if (this.sendButton) {
            this.sendButton.addEventListener('click', () => this.sendMessage());
        }

        // Input field events
        if (this.messageInput) {
            this.messageInput.addEventListener('input', () => this.updateSendButtonState());
            this.messageInput.addEventListener('keypress', (e) => this.handleKeyPress(e));
            this.messageInput.addEventListener('paste', () => {
                setTimeout(() => this.updateSendButtonState(), 10);
            });
        }

        // Window resize
        window.addEventListener('resize', () => this.scrollToBottom());
    }

    /**
     * Handle keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Enter to send message
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                this.sendMessage();
            }

            // Escape to focus input
            if (e.key === 'Escape') {
                this.focusInput();
            }
        });
    }

    /**
     * Initialize auto-resize for input
     */
    initializeAutoResize() {
        if (this.messageInput) {
            this.messageInput.style.height = 'auto';
            this.messageInput.addEventListener('input', () => {
                this.messageInput.style.height = 'auto';
                this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
            });
        }
    }

    /**
     * Handle key press events
     */
    handleKeyPress(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }

    /**
     * Update send button state based on input
     */
    updateSendButtonState() {
        if (!this.sendButton || !this.messageInput) return;

        const hasText = this.messageInput.value.trim().length > 0;
        const isValid = this.messageInput.value.length <= this.config.maxMessageLength;

        this.sendButton.disabled = !hasText || !isValid || this.isProcessing;

        // Update button appearance
        if (this.isProcessing) {
            this.sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        } else {
            this.sendButton.innerHTML = '<i class="fas fa-paper-plane"></i> Send';
        }
    }

    /**
     * Send a message
     */
    async sendMessage() {
        const message = this.messageInput.value.trim();

        if (!message || this.isProcessing) return;

        // Validate message length
        if (message.length > this.config.maxMessageLength) {
            this.showError(`Message too long. Maximum ${this.config.maxMessageLength} characters allowed.`);
            return;
        }

        this.isProcessing = true;
        this.updateSendButtonState();

        try {
            // Clear input immediately
            this.messageInput.value = '';
            this.messageInput.style.height = 'auto';

            // Add user message to chat
            this.addMessage(message, 'user');

            // Show typing indicator
            this.showTypingIndicator();

            // Send to server
            const response = await this.sendToServer(message);

            // Hide typing indicator
            this.hideTypingIndicator();

            // Add bot response
            this.addMessage(response.bot_response, 'bot', response);

            // Handle any special responses
            this.handleSpecialResponses(response);

        } catch (error) {
            this.hideTypingIndicator();
            console.error('Error sending message:', error);

            let errorMessage = 'Sorry, I encountered an error. Please try again.';
            if (error.message) {
                errorMessage = `Error: ${error.message}`;
            }

            this.addMessage(errorMessage, 'bot', { is_error: true });
        } finally {
            this.isProcessing = false;
            this.updateSendButtonState();
            this.focusInput();
        }
    }

    /**
     * Send quick question
     */
    sendQuickQuestion(question) {
        if (this.messageInput) {
            this.messageInput.value = question;
            this.updateSendButtonState();
            this.sendMessage();
        }
    }

    /**
     * Send message to server
     */
    async sendToServer(message) {
        try {
            // Get CSRF token from multiple possible sources
            let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

            if (!csrfToken) {
                csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
            }

            if (!csrfToken) {
                // Try to get from cookies
                const cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    const [name, value] = cookie.trim().split('=');
                    if (name === 'csrftoken') {
                        csrfToken = value;
                        break;
                    }
                }
            }

            console.log('Sending message to server:', message);
            console.log('CSRF Token found:', csrfToken ? 'Yes' : 'No');

            // Send message to server
            const response = await fetch('/process-message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken || '',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ message: message })
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Server response error:', errorText);
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }

            const data = await response.json();
            console.log('Server response:', data);
            return data;

        } catch (error) {
            console.error('Network error in sendToServer:', error);
            throw error;
        }
    }

    /**
     * Add message to chat
     */
    addMessage(content, type, metadata = {}) {
        if (!this.chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type === 'user' ? 'user-message' : 'bot-message'}`;

        if (metadata.is_urgent) {
            messageDiv.classList.add('crisis-message');
        }

        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>
                    ${type === 'user' 
                        ? '<i class="fas fa-user"></i> You' 
                        : '<i class="fas fa-graduation-cap"></i> University Guide'}:
                </strong>
                <div class="mt-1">${this.formatMessage(content)}</div>
            </div>
            <div class="message-time">${timestamp}</div>
        `;

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();

        // Add to history
        this.messageHistory.push({ type, content, timestamp: new Date() });
    }

    /**
     * Format message content
     */
    formatMessage(content) {
        // Convert line breaks to HTML
        let formatted = content.replace(/\n/g, '<br>');

        // Make URLs clickable
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        formatted = formatted.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');

        // Make bold text
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        return formatted;
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        if (this.typingIndicator) {
            this.typingIndicator.style.display = 'block';
            this.scrollToBottom();
        }
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        if (this.typingIndicator) {
            this.typingIndicator.style.display = 'none';
        }
    }

    /**
     * Handle special responses
     */
    handleSpecialResponses(response) {
        if (response.is_urgent && response.relevant_resources) {
            this.showCrisisModal(response.relevant_resources);
        }
    }

    /**
     * Show crisis modal
     */
    showCrisisModal(resources) {
        const modal = document.getElementById('crisisModal');
        if (modal) {
            const resourcesDiv = document.getElementById('crisis-resources');
            if (resourcesDiv) {
                resourcesDiv.innerHTML = resources.map(resource => `
                    <div class="mb-3">
                        <h6>${resource.title}</h6>
                        <p>${resource.description}</p>
                        ${resource.url ? `<a href="${resource.url}" target="_blank" class="btn btn-sm btn-primary">Learn More</a>` : ''}
                    </div>
                `).join('');
            }

            // Show modal using Bootstrap
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        }
    }

    /**
     * Show error message
     */
    showError(message) {
        this.addMessage(message, 'bot', { is_error: true });
    }

    /**
     * Scroll to bottom of chat
     */
    scrollToBottom() {
        if (this.chatMessages) {
            setTimeout(() => {
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            }, 100);
        }
    }

    /**
     * Focus input field
     */
    focusInput() {
        if (this.messageInput && !this.isProcessing) {
            setTimeout(() => this.messageInput.focus(), 100);
        }
    }

    /**
     * Load chat history (placeholder)
     */
    loadChatHistory() {
        // This would load existing messages from the server
        console.log('Chat history loaded');
    }

    /**
     * Clear chat
     */
    clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            window.location.href = '/chat/clear/';
        }
    }
}

// Global functions for HTML event handlers
function sendMessage() {
    if (window.chatbot) {
        window.chatbot.sendMessage();
    }
}

function sendQuickQuestion(question) {
    if (window.chatbot) {
        window.chatbot.sendQuickQuestion(question);
    }
}

function handleKeyPress(event) {
    if (window.chatbot) {
        window.chatbot.handleKeyPress(event);
    }
}

function clearChat() {
    if (window.chatbot) {
        window.chatbot.clearChat();
    }
}

function dismissQuickButton(dismissBtn) {
    const quickButtonItem = dismissBtn.closest('.quick-button-item');
    if (quickButtonItem) {
        // Add fade out animation
        quickButtonItem.style.transition = 'all 0.3s ease';
        quickButtonItem.style.opacity = '0';
        quickButtonItem.style.transform = 'scale(0.8)';
        
        // Remove after animation
        setTimeout(() => {
            quickButtonItem.remove();
            
            // Check if container is empty and hide it
            const container = document.getElementById('quick-buttons-container');
            if (container && container.children[0].children.length === 0) {
                container.style.display = 'none';
            }
        }, 300);
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.chatbot = new UniversityGuidanceChatbot();
});