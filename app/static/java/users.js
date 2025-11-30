
window.addEventListener('load', function () 
{
    const admin=document.getElementById('superstatus');
    const campusSelect = document.getElementById('campus2');
    campusSelect.addEventListener('change', function() {
        const banner = document.getElementById('banner-name').textContent;
        if (admin.checked && banner === "Users") {
            usersRequest();
        }
    });
});
function usersRequest()
{
    let campus = document.getElementById("campus-name").textContent;
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const temp=document.getElementById('campus2').value;
        document.getElementById('campus-name').textContent=temp;
        campus=temp;
    }
    fetch(`${API_URL}/users_request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ campus })
    })
    .then(response => response.json())
    .then(data => {
        const users = data.users || [];
        updateUsers(users);
    })
    .catch(err => console.error("Products request failed:", err));
}
function updateUsers(users)
{
    const container = document.getElementById("users_container");
    container.innerHTML = "";

    users.forEach(user => {
        const userStr = JSON.stringify(user).replace(/'/g, "&apos;");
        container.innerHTML += `
            <div class="data" onclick='editUser(${userStr})'>
                <div style=" justify-content: center;">
                    <input type="checkbox" name="select" value="no" ${user.active ? "checked" : ""} disabled>
                </div>
                <div>${ user.id }</div>
                <div style="align-items: center; display: flex;">
                    <span>${ user.name }</span>
                </div>
                <div>${ user.email }</div>
                <div>${ user.password }%</div>
            </div>
        `;
    });
}
function editUser(user)
{
    document.getElementById('userName').value = user.name || '';
    document.getElementById('userEmail').value = user.email || '';
    document.getElementById('userPassword').value = '';
    document.getElementById('userCampus').value = user.campus_id || '';
    document.getElementById('userRole').value = user.clearance_level || '';
    document.getElementById('userActive').checked = user.active || false;
    document.getElementById('userStart').value = user.start_date || '';
    document.getElementById('userEnd').value = user.end_date || '';
    document.getElementById('userId').value = user.id;
    document.getElementById('user-banner').textContent='Edit User';
    document.getElementById('user-button').textContent='Edit';
}
function saveUser()
{
    const name = document.getElementById('userName').value.trim();
    const email = document.getElementById('userEmail').value.trim();
    const userId = document.getElementById('userId').value;
    const password = document.getElementById('userPassword').value.trim();
    const campus = document.getElementById('userCampus').value;
    const role = document.getElementById('userRole').value;
    const active = document.getElementById('userActive').checked;
    const start = document.getElementById('userStart').value.trim();
    const end = document.getElementById('userEnd').value.trim();
    const banner = document.getElementById('user-banner').textContent;
    if(name==="")
    {
        alert("Please input the name!");
        return;
    }if(password==="")
    {
        alert("Please input the password!");
        return;
    }
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) 
    {
        alert("Please enter a valid email address!");
        return;
    }
    if(campus=="")
    {
        alert("Please select a campus!");
        return;
    }
    if(role=="")
    {
        alert("Please select a role!");
        return;
    }
    if(start=="")
    {
        alert("Please select the start date!");
        return;
    }
    if(end=="")
    {
        alert("Please select the end date!");
        return;
    }
    if(start>end)
    {
        alert("Please select a valid date range!");
        return;
    }
        const formData = new FormData();
        if (userId) formData.append('user_id', userId);
        formData.append('name', name);
        formData.append('email', email);
        formData.append('password', password);
        formData.append('campus_id', campus);
        formData.append('clearance_level', role);
        formData.append('start_date', start);
        formData.append('end_date', end);
        fetch('/admin/add_user', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if(banner==='Add User')
                {
                    alert('User saved successfully!');
                }
                else
                {
                    alert('User updated successfully!');
                }
                resetUserForm();
                usersRequest();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => alert('Error: ' + error));
}
function resetUserForm() {
    document.getElementById('userName').value = '';
    document.getElementById('userEmail').value = '';
    document.getElementById('userId').value = '';
    document.getElementById('userPassword').value = '';
    document.getElementById('userCampus').value = '';
    document.getElementById('userRole').value = '';
    document.getElementById('userActive').checked = false;
    document.getElementById('userStart').value = '';
    document.getElementById('userEnd').value = '';
    document.getElementById('user-banner').textContent='Add User';
    document.getElementById('user-button').textContent='Add';
}