window.addEventListener('load', function () {
    const admin = document.getElementById('superstatus');
    if (admin && admin.checked) {
        const campusSelect = document.getElementById('campus2');
        const banner = document.getElementById('banner-name').value;
        if (banner === "Users") {
            campusSelect.addEventListener('change', function () {
                usersRequest();
            });
        }
    }
});

function usersRequest() {
    // Implement AJAX user list refresh if needed
}

function editUser(id, name, email, campus_id, clearance_level, start_date, end_date, active) {
    document.getElementById('userForm').action = '/user/edit/' + id;
    document.getElementById('userId').value = id;
    document.getElementById('userName').value = name;
    document.getElementById('userEmail').value = email;
    document.getElementById('userCampus').value = campus_id;
    document.getElementById('userRole').value = clearance_level;
    document.getElementById('userStart').value = start_date;
    document.getElementById('userEnd').value = end_date;

    // Checkbox logic: checked if inactive (active == 0, "0", or false)
    // OR if today is outside start/end date
    const userActiveCheckbox = document.getElementById('userActive');
    let isInactive = (active == 0 || active === "0" || active === false);

    // Date-based logic
    const today = new Date();
    let startValid = true, endValid = true;
    if (start_date) {
        const start = new Date(start_date);
        startValid = today >= start;
    }
    if (end_date) {
        const end = new Date(end_date);
        endValid = today <= end;
    }
    // If both dates are set and today is not within range, mark as inactive
    if (start_date && end_date && (!startValid || !endValid)) {
        isInactive = true;
    }

    userActiveCheckbox.checked = isInactive;
}

function resetUserForm() {
    document.getElementById('userForm').action = '/user/add';
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';
    document.getElementById('userActive').checked = false;
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