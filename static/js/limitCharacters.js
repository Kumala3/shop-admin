document.addEventListener("DOMContentLoaded", function () {
    // Since `getElementsByClassName` returns a HTMLCollection, we need to select the first element
    const messageInput = document.getElementsByClassName("message-input")[0];
    const charCounter = document.getElementsByClassName("char-counter")[0];
    const submitButton =
        document.getElementsByClassName("submit-button")[0];
    const limit = 4096;

    // Function to update the character counter
    function updateCharCounter() {
        const textLength = messageInput.value.length;
        charCounter.textContent = `${textLength}/${limit}`; // Update the counter display

        // Logic for when text length exceeds the limit
        if (textLength > limit) {
            messageInput.style.borderColor = "#ff2851";
            charCounter.style.color = "#ff2851";
            submitButton.disabled = true;
        } else {
            messageInput.style.borderColor = ""; // Reset border color
            charCounter.style.color = ""; // Reset text color
            submitButton.disabled = false;
        }
    }

    // Event listener for input on the textarea to update the counter as the user types
    messageInput.addEventListener("input", updateCharCounter);
});
