/**
 * CHUCHUREX - Chat Application
 * Frontend JavaScript
 */

const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://127.0.0.1:8002'
    : 'https://api.chuchurex.cl';

// DOM Elements
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');

// Conversation history for context
let conversationHistory = [];

// Current language
let currentLang = 'es';

// =============================================================================
// CHAT FUNCTIONS
// =============================================================================

/**
 * Send message to backend and get response
 */
async function sendMessage(message) {
    // Add user message to history
    conversationHistory.push({
        role: 'user',
        content: message
    });

    // Display user message
    displayMessage(message, 'user');

    // Show typing indicator
    const typingIndicator = showTypingIndicator();

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory.slice(-10), // Last 10 messages for context
                lang: currentLang
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Remove typing indicator
        typingIndicator.remove();

        // Add assistant message to history
        conversationHistory.push({
            role: 'assistant',
            content: data.response
        });

        // Display assistant message
        displayMessage(data.response, 'assistant');

        // Si se debe generar PDF, mostrar indicador de carga
        if (data.generate_pdf && data.pdf_url) {
            const loadingIndicator = displayPDFLoadingIndicator();

            // Esperar mientras se genera el PDF
            setTimeout(() => {
                loadingIndicator.remove();
                displayPDFDownloadLink(data.pdf_url);
            }, 3000); // 3 segundos para dar tiempo a la generación
        }

    } catch (error) {
        console.error('Error:', error);
        typingIndicator.remove();
        displayMessage(window.i18n.t('errorGeneric'), 'assistant');
    }
}

/**
 * Display a message in the chat
 */
function displayMessage(content, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${role}`;

    // Parse markdown-like formatting for assistant messages
    if (role === 'assistant') {
        messageDiv.innerHTML = formatMessage(content);
    } else {
        messageDiv.textContent = content;
    }

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Format message with basic markdown support
 */
function formatMessage(text) {
    // Split into paragraphs
    const paragraphs = text.split('\n\n');

    return paragraphs.map(p => {
        // Bold
        p = p.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Italic
        p = p.replace(/\*(.*?)\*/g, '<em>$1</em>');
        // Line breaks within paragraph
        p = p.replace(/\n/g, '<br>');
        return `<p>${p}</p>`;
    }).join('');
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    chatMessages.appendChild(indicator);
    scrollToBottom();
    return indicator;
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Display PDF loading indicator
 */
function displayPDFLoadingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-assistant message-pdf-loading';

    messageDiv.innerHTML = `
        <div class="pdf-loading-content">
            <div class="pdf-spinner"></div>
            <p>${window.i18n.t('pdfLoading')}</p>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    return messageDiv;
}

/**
 * Display PDF download link
 */
function displayPDFDownloadLink(pdfUrl) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-assistant message-pdf';

    const downloadLink = `${API_URL}${pdfUrl}`;

    messageDiv.innerHTML = `
        <p>✅ <strong>${window.i18n.t('pdfReady')}</strong></p>
        <a href="${downloadLink}" class="pdf-download-button" target="_blank" download>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            ${window.i18n.t('pdfDownload')}
        </a>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// =============================================================================
// TEXTAREA AUTO-RESIZE
// =============================================================================

function autoResize() {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
}

// =============================================================================
// EVENT LISTENERS
// =============================================================================

// Form submit
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = userInput.value.trim();
    if (!message) return;

    // Disable input while sending
    userInput.disabled = true;
    sendButton.disabled = true;

    // Clear input
    userInput.value = '';
    autoResize();

    // Send message
    await sendMessage(message);

    // Re-enable input
    userInput.disabled = false;
    sendButton.disabled = false;
    userInput.focus();
});

// Textarea auto-resize
userInput.addEventListener('input', autoResize);

// Submit on Enter (but Shift+Enter for new line)
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

// =============================================================================
// INITIALIZATION
// =============================================================================

// Header scroll effect
const header = document.querySelector('.header');
const scrollContainer = document.querySelector('.chat-messages');

if (scrollContainer) {
    scrollContainer.addEventListener('scroll', () => {
        if (scrollContainer.scrollTop > 20) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

// Initialize i18n and apply translations
window.addEventListener('DOMContentLoaded', () => {
    currentLang = window.i18n.getCurrentLanguage();
    window.i18n.applyTranslations(currentLang);
});

// Focus input on load
window.addEventListener('load', () => {
    userInput.focus();
});
