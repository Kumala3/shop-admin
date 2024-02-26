document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementsByClassName(".message-input");

    textarea.oninvalid = function (event) {
        event.target.setCustomValidity(
            "Заполните сообщение перед отправкой"
        );
    };

    textarea.oninput = function (event) {
        // Clear the custom validity message once the user starts typing
        event.target.setCustomValidity("");
    };
});
