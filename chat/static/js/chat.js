let socket = new WebSocket("ws://127.0.0.1:8000/ws/chat/");

socket.onopen = function() {
    console.log("WebSocket connected");
    loadChatHistory(); // Load previous messages from localStorage
};

socket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    let chatBox = document.getElementById("chatBox");

    if (data.response) {
        let botMessage = document.createElement("p");
        botMessage.className = "message bot-message";
        botMessage.innerHTML = data.response;
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight;

        document.getElementById("typingIndicator").style.display = "none";
        saveChatHistory();
    } else if (data.error) {
        alert("Error: " + data.error);
    }
};

function sendMessage() {
    let userInput = document.getElementById("userInput").value.trim();
    if (userInput === "") return;

    let chatBox = document.getElementById("chatBox");

    let userMessage = document.createElement("p");
    userMessage.className = "message user-message";
    userMessage.innerHTML = userInput;
    chatBox.appendChild(userMessage);

    document.getElementById("userInput").value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    document.getElementById("typingIndicator").style.display = "block";

    socket.send(JSON.stringify({ message: userInput }));
    saveChatHistory();
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function saveChatHistory() {
    let chatBox = document.getElementById("chatBox").innerHTML;
    localStorage.setItem("chatMessages", chatBox);
}

function loadChatHistory() {
    localStorage.removeItem("chatMessages");
    document.getElementById("chatBox").innerHTML = "";
}
