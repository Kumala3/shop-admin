import axios from "axios";

function getSelectedUserIds() {
    // Get all checkboxes that are checked
    const checkedCheckboxes = document.querySelectorAll(
        'input[type="checkbox"]:checked'
    );

    // Extract the user IDs from the value attribute of the checkboxes
    const userIds = Array.from(checkedCheckboxes).map(
        checkbox => checkbox.value
    );

    return userIds;
}


async function sendUserIds(userIds) {
    try {
        const response = await axios.post(
            "http:/localhost:8000/get_users_ids",
            {
                userIds: userIds,
            }
        );

        console.log("Data received:", response.data);
    } catch (error) {
        console.error("Failed to send user IDs:", error);
    }
}

const selectedUserIds = getSelectedUserIds();
sendUserIds(selectedUserIds);
