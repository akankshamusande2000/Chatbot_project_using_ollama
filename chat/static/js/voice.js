function startVoiceInput() {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';

        recognition.onstart = function() {
            console.log("Speech recognition started...");
        };

        recognition.onend = function() {
            document.getElementById("typingIndicator").style.display = "block";
        };

        recognition.onresult = function(event) {
            let userInput = event.results[0][0].transcript.trim();
            if (userInput !== "") {
                let chatBox = document.getElementById("chatBox");
                let userMessage = document.createElement("p");
                userMessage.className = "message user-message";
                userMessage.innerHTML = userInput;
                chatBox.appendChild(userMessage);
                chatBox.scrollTop = chatBox.scrollHeight;

                socket.send(JSON.stringify({ message: userInput }));

                document.getElementById("typingIndicator").style.display = "block";
                saveChatHistory();
            }
        };

        recognition.start();
    }
}
