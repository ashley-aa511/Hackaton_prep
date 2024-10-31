// Function to handle adding a user
document.getElementById('addUserForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent page refresh
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;

    const response = await fetch('http://127.0.0.1:5000/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, age: parseInt(age) }),
    });

    const result = await response.json();
    alert(result.message); // Display response message
    fetchUsers(); // Refresh the user list after adding
});

// Function to fetch and display all users
async function fetchUsers() {
    const response = await fetch('http://127.0.0.1:5000/users');
    const users = await response.json();

    const userList = document.getElementById('userList');
    userList.innerHTML = ''; // Clear current list
    users.forEach(user => {
        const listItem = document.createElement('li');
        listItem.textContent = `${user.name} (Age: ${user.age}) `;

        // Create Delete button
        const deleteButton = document.createElement('button');
        deleteButton.textContent = "Delete";
        deleteButton.onclick = () => deleteUser(user.id); // Attach delete function
        listItem.appendChild(deleteButton);

        // Create Edit button
        const editButton = document.createElement('button');
        editButton.textContent = "Edit";
        editButton.onclick = () => showEditForm(user.id, user.name, user.age); // Attach edit function
        listItem.appendChild(editButton);

        userList.appendChild(listItem);
    });
}

// Function to handle deleting a user
async function deleteUser(userId) {
    const response = await fetch(`http://127.0.0.1:5000/delete/${userId}`, {
        method: 'DELETE',
    });

    const result = await response.json();
    alert(result.message); // Show success or error message
    fetchUsers(); // Refresh the user list after deletion
}

// Function to show the edit form with current user data
function showEditForm(userId, currentName, currentAge) {
    // Populate the form fields with current user data
    document.getElementById('editUserId').value = userId;
    document.getElementById('editName').value = currentName;
    document.getElementById('editAge').value = currentAge;

    // Show the edit form
    document.getElementById('editUserForm').style.display = 'block';
}

// Function to handle updating a user
document.getElementById('updateUserForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent page refresh
    const userId = document.getElementById('editUserId').value;
    const updatedName = document.getElementById('editName').value;
    const updatedAge = document.getElementById('editAge').value;

    const response = await fetch(`http://127.0.0.1:5000/update/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: updatedName, age: parseInt(updatedAge) }),
    });

    const result = await response.json();
    alert(result.message); // Show success or error message

    // Hide the edit form and refresh the user list
    document.getElementById('editUserForm').style.display = 'none';
    fetchUsers();
});

// Function to handle searching for a user by name
document.getElementById('searchForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent page refresh
    const searchName = document.getElementById('searchName').value;

    const response = await fetch(`http://127.0.0.1:5000/search?name=${searchName}`);
    const searchResults = await response.json();

    const resultsList = document.getElementById('searchResults');
    resultsList.innerHTML = ''; // Clear current list

    if (Array.isArray(searchResults)) {
        searchResults.forEach(user => {
            const listItem = document.createElement('li');
            listItem.textContent = `${user.name} (Age: ${user.age})`;
            resultsList.appendChild(listItem);
        });
    } else {
        // Display message if no users are found
        resultsList.textContent = searchResults.message || "No users found";
    }
});
