const chatBox = document.getElementById("chat");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("send-btn");
const newChatButton = document.getElementById("new-chat-btn");

// CONVERSATION DATA
let conversations = [];
let currentConversationId = null;

// LOCAL STORAGE
function saveConversations() {
    localStorage.setItem(
        "uniqConversations",
        JSON.stringify(conversations)
    );
}


function loadConversations() {

    const saved = localStorage.getItem("uniqConversations");

    if (saved) {
        conversations = JSON.parse(saved);
    }
}

// MESSAGE DISPLAY
function addMessage(text, who) {

    const newMessage = document.createElement("div");

    newMessage.className = "message " + who;
    newMessage.innerText = text;

    chatBox.appendChild(newMessage);

    scrollToBottom();
}

// CREATE NEW CHAT
function newChat() {

    const conversation = {
        id: Date.now(),
        title: "New Chat",
        messages: []
    };

    conversations.unshift(conversation);

    currentConversationId = conversation.id;

    saveConversations();
    renderHistory();
    clearChat();

    messageInput.focus();
}

// CLEAR CHAT WINDOW
function clearChat() {

    chatBox.innerHTML = `
        <div class="message bot">
            Hello! I am UNIQ, your AI chatbot.
            How can I assist you today?
        </div>
    `;

}


// SAVE MESSAGE
function saveMessage(sender, text) {

    const conversation = conversations.find(
        function(conversation) {
            return conversation.id === currentConversationId;
        }
    );

    if (!conversation) {
        return;
    }

    conversation.messages.push({
        sender: sender,
        text: text
    });

    // Use first user message as conversation title
    if (sender === "user" && conversation.title === "New Chat") {

        conversation.title = text.substring(0, 30);

        if (text.length > 30) {
            conversation.title += "...";
        }
    }

    saveConversations();
    renderHistory();
}

// LOAD OLD CONVERSATION
function loadConversation(id) {

    const conversation = conversations.find(
        function(conversation) {
            return conversation.id === id;
        }
    );

    if (!conversation) {
        return;
    }

    currentConversationId = id;

    chatBox.innerHTML = "";

    conversation.messages.forEach(
        function(message) {

            addMessage(
                message.text,
                message.sender
            );

        }
    );

    scrollToBottom();
}

// DISPLAY CHAT HISTORY
function renderHistory() {

    const historyList = document.getElementById("history-list");

    if (!historyList) {
        return;
    }

    historyList.innerHTML = "";

    conversations.forEach(
        function(conversation) {

            const item = document.createElement("button");

            item.className = "history-item";

            item.innerText = conversation.title;

            item.addEventListener(
                "click",
                function() {

                    loadConversation(conversation.id);

                }
            );

            historyList.appendChild(item);

        }
    );
}

// SEND MESSAGE
function sendMessage() {

    const text = messageInput.value.trim();

    if (text === "") {
        return;
    }


    // If there is no active conversation,
    // automatically create one
    if (currentConversationId === null) {
        newChat();
    }

    // Show user's message
    addMessage(text, "user");

    // Save user's message
    saveMessage("user", text);

    // Clear input
    messageInput.value = "";

    // Show typing indicator
    showTypingIndicator();


    // Disable button while waiting
    sendButton.disabled = true;


    // Send message to Flask
    fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: text
        })

    })

    .then(function(response) {

        return response.json();

    })

    .then(function(data) {

        // Remove typing animation
        removeTypingIndicator();

        // Show bot response
        addMessage(data.reply, "bot");

        // Save bot response
        saveMessage("bot", data.reply);

    })

    .catch(function(error) {

        console.error("Error:", error);

        removeTypingIndicator();

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

    })

    .finally(function() {

        // Enable button again
        sendButton.disabled = false;

        messageInput.focus();

    });
}

// TYPING INDICATOR
function showTypingIndicator() {

    const typing = document.createElement("div");

    typing.className = "message bot typing";
    typing.id = "typing";

    typing.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;

    chatBox.appendChild(typing);

    scrollToBottom();
}


function removeTypingIndicator() {

    const typing = document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}

// AUTO SCROLL
function scrollToBottom() {

    chatBox.scrollTop = chatBox.scrollHeight;

}

// EVENT LISTENERS
sendButton.addEventListener(
    "click",
    sendMessage
);


messageInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


newChatButton.addEventListener(
    "click",
    newChat
);

// INITIALIZE
loadConversations();

renderHistory();


// load existing conversation if available, otherwise start a new chat
if (conversations.length > 0) {

    loadConversation(
        conversations[0].id
    );

} else {

    newChat();

}