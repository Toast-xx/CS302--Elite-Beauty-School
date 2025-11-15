function ordersRequest()
{
    const start_date = document.getElementById("startdate").value;
    const end_date = document.getElementById("enddate").value;
    const campus = document.getElementById("campus-name").value;
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const temp=document.getElementById('campus').value;
        document.getElementById('campus-name').value=temp;
        campus=temp;
    }
    fetch("/orders_request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start_date, end_date, campus })
    })
    .then(response => response.json())
    .then(data => {
        updateOrders(data);
    })
    .catch(err => console.error("Orders request failed:", err));
}
function updateOrders(data)
{
    const container = document.getElementById("orders_container");
    container.innerHTML = "";
    data.forEach(item => {
        const statusClass =
            item.status === "Completed" ? "completed" :
            item.status === "Cancelled" ? "cancelled" :
            item.status === "Pending" ? "pending" :
            item.status === "Refunded" ? "refunded" : "";

        container.innerHTML += `
            <div class="value">
                <div>${item.id}</div>
                <div>${item.date}</div>
                <div>${item.percentage}%</div>
                <div>${item.amount}</div>
                <div class="${statusClass}">${item.status}</div>
            </div>
        `;
    });
}