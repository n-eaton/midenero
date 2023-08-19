document.addEventListener('DOMContentLoaded', function () {
    // Get the messages container
    const messagesContainer = document.getElementById('flash-messages');

    // Set a timeout to hide the messages after 5 seconds
    setTimeout(function () {
        messagesContainer.style.display = 'none';
    }, 1000); // 1000 milliseconds = 1 second
});