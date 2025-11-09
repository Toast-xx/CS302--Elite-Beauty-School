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