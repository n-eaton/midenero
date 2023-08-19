document.addEventListener('DOMContentLoaded', function () {
    // Get the messages container
    const messagesContainer = document.getElementById('flash-messages');

    // Set a timeout to hide the messages after 5 seconds
    setTimeout(function () {
        messagesContainer.style.display = 'none';
    }, 5000); // 5000 milliseconds = 5 seconds
});