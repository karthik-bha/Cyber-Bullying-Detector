document.addEventListener('DOMContentLoaded', function() {
    // Initialize Socket.IO connection
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Function to send the message when the 'Send' button is clicked
    document.getElementById("sendBtn").addEventListener("click", function() {
        var messageText = document.getElementById("messageInput").value;
        var user = "User";  // You can replace this with the actual user's name or ID if necessary

        // Emit message to the server
        if (messageText) {
            console.log("Sending message:", messageText); // Debugging log
            socket.emit('message', {
                message: messageText,
                user: user
            });

            // Clear the input after sending
            document.getElementById("messageInput").value = '';
        }
    });

    // Listen for messages from the server
    socket.on('message', function(data) {
        console.log('Message received from server:', data);  // Debugging log
        var messageDiv = document.createElement('div');
        messageDiv.classList.add('message');

        // Check if the message is cyberbullying and set the appropriate color
        var cyberbullyingClass = data.cyberbullying === "Cyberbullying Detected" ? "cyberbullying-flagged" : "cyberbullying-safe";
        
        messageDiv.innerHTML = "<strong>" + data.user + ":</strong> " + data.message + 
                               " <span class='" + cyberbullyingClass + "'>" + data.cyberbullying + "</span>";
        document.getElementById('chatBox').appendChild(messageDiv);
    });
});
