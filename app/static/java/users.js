const API_URL = "https://elite-emporium.onrender.com";
window.addEventListener('load', function () 
{
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const campusSelect = document.getElementById('campus2');
        const banner=document.getElementById('banner-name').textContent;
        if(banner==="Users")
        {
            campusSelect.addEventListener('change', function() {
                usersRequest();
            });
        }
    }
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
                    <img style="width: 40px; height: 40px; margin-right: 10px; border-radius: 100px;" src="{{ url_for('static', filename='images/dummy.png') }}">
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
    alert(user.id);
}
function saveUser()
{
    const name=document.getElementById('userName');
    const email=document.getElementById('userEmail');
    const campus=document.getElementById('userCampus');
    const role=document.getElementById('userRole');
    const active=document.getElementById('userActive');
    const start=document.getElementById('userStart');
    const end=document.getElementById('userEnd');
    if(name.value.trim()==="")
    {
        alert("Please input the name!");
        return;
    }
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email.value)) 
    {
        alert("Please enter a valid email address!");
        return;
    }
    if(campus.value=="")
    {
        alert("Please select a campus!");
        return;
    }
    if(role.value=="")
    {
        alert("Please select a role!");
        return;
    }
    if(start.value=="")
    {
        alert("Please select the start date!");
        return;
    }
    if(end.value=="")
    {
        alert("Please select the end date!");
        return;
    }
    if(start.value>end.value)
    {
        alert("Please select a valid date range!");
        return;
    }
}