const chatContainer = document.getElementById('chat-container');
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const toggleButton = document.getElementById('chat-toggle-button');

// Toggle chat window visibility
toggleButton.addEventListener('click', () => {
    const isHidden = chatContainer.style.display === 'none' || chatContainer.style.display === '';
    chatContainer.style.display = isHidden ? 'flex' : 'none';
    // Optional: Change button icon based on state
    // toggleButton.textContent = isHidden ? '✕' : '💬';
});

// Function to add a message to the chat box
function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'ai-message');
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    // Scroll to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to handle sending a message
async function sendMessage() {
    const messageText = userInput.value.trim();
    if (messageText === '') return;

    // Disable input and button while sending
    userInput.disabled = true;
    sendButton.disabled = true;
    sendButton.textContent = '发送中...';

    // Add user message to chat box
    addMessage(messageText, 'user');
    userInput.value = ''; // Clear input field
    userInput.style.height = '20px'; // Reset textarea height

    try {
        // Send message to backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: messageText }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Add AI response to chat box
        addMessage(data.reply, 'ai');

    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('抱歉，发送消息时出错，请稍后再试。', 'ai');
    } finally {
        // Re-enable input and button
        userInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = '发送';
        userInput.focus(); // Set focus back to input
    }
}

// Event listener for send button click
sendButton.addEventListener('click', sendMessage);

// Event listener for Enter key press in textarea (Shift+Enter for newline)
userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault(); // Prevent default Enter behavior (newline)
        sendMessage();
    }
});

// Auto-resize textarea based on content
// Close chat window when clicking outside (optional)
/*
document.addEventListener('click', (event) => {
    if (!chatContainer.contains(event.target) && !toggleButton.contains(event.target)) {
        chatContainer.style.display = 'none';
        // toggleButton.textContent = '💬';
    }
});
*/

userInput.addEventListener('input', () => {
    userInput.style.height = 'auto'; // Reset height
    userInput.style.height = `${userInput.scrollHeight}px`; // Set to scroll height
});