
function ordersRequest()
{
    const start_date = document.getElementById("startdate").value;
    const end_date = document.getElementById("enddate").value;
    let campus = document.getElementById("campus-name").textContent;
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const temp=document.getElementById('campus').value;
        document.getElementById('campus-name').textContent=temp;
        campus=temp;
    }
    fetch(`${API_URL}/orders_request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ start_date, end_date, campus })
    })
    .then(response => response.json())
    .then(data => {
        const orders = data.orders || [];
        updateOrders(orders);
    })
    .catch(err => console.error("Orders request failed:", err));
}
function updateOrders(data) {
    const container = document.getElementById("orders_container");
    container.innerHTML = "";
    data.forEach(item => {
        const statusClass =
            item.status === "Completed" ? "completed" :
                item.status === "Cancelled" ? "cancelled" :
                    item.status === "Pending" ? "pending" :
                        item.status === "Refunded" ? "refunded" : "";

        // Status options
        const statusOptions = ["Paid", "Pending", "Completed", "Cancelled", "Refunded"];
        const statusSelect = `
            <select onchange="updateOrderStatus(${item.id}, this.value)">
                ${statusOptions.map(opt =>
            `<option value="${opt}"${opt === item.status ? " selected" : ""}>${opt}</option>`
        ).join("")}
            </select>
        `;

        container.innerHTML += `
            <div class="value">
                <div>${item.id}</div>
                <div>${item.created_at}</div>
                <div>${item.promotion || ""}</div>
                <div>$${item.total}</div>
                <div class="${statusClass}">${statusSelect}</div>
            </div>
        `;
    });
}
function updateOrderStatus(orderId, status) {
    fetch(`${API_URL}/update_order_status`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ order_id: orderId, status })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Order status updated!");
                ordersRequest(); // Refresh the orders list
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(err => alert("Error: " + err));
}