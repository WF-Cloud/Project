var chatBox = document.getElementById("chat");
var messageInput = document.getElementById("message");
var sendButton = document.getElementById("send-btn");

function addMessage(text, who) {
    var newMessage = document.createElement("div");
    newMessage.className = "message " + who;
    newMessage.innerText = text;
    chatBox.appendChild(newMessage);
}

function sendMessage() {
    var text = messageInput.value;

    if (text.trim() === "") {
        return;
    }

    addMessage(text, "user");
    messageInput.value = "";

    addMessage("I hear you! We will connect this to flask next.", "bot");
}

sendButton.onclick = sendMessage;

messageInput.onkeydown = function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}