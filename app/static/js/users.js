function editUser(id, name, email, campus_id, clearance_level, start_date, end_date) {
    document.getElementById('userForm').action = '/user/edit/' + id; // <-- Set to edit endpoint
    document.getElementById('userId').value = id;
    document.getElementById('userName').value = name;
    document.getElementById('userEmail').value = email;
    document.getElementById('userCampus').value = campus_id;
    document.getElementById('userRole').value = clearance_level;
    document.getElementById('userStart').value = start_date;
    document.getElementById('userEnd').value = end_date;
}

function resetUserForm() {
    document.getElementById('userForm').action = '/user/add'; // <-- Set to add endpoint
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';
}

document.getElementById('userForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showPopup("Error", data.error);
            } else if (data.message) {
                showPopup("Success", data.message);
                resetUserForm();
            }
        })
        .catch(err => {
            showPopup("Error", "An unexpected error occurred.");
        });
});

function showPopup(title, message) {
    // If you use the default overlay, update its content
    let popup = document.getElementById('popup');
    let overlay = document.getElementById('successUserOverlay');
    let popupTitle = overlay.querySelector('h2');
    let popupMessage = overlay.querySelector('.middle span');
    popupTitle.textContent = title;
    popupMessage.textContent = message;
    popup.style.display = 'flex';
    overlay.classList.add('active');
}

function closeSuccessOverlay() {
    let popup = document.getElementById('popup');
    let overlay = document.getElementById('successUserOverlay');
    popup.style.display = 'none';
    overlay.classList.remove('active');
}