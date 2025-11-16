const API_URL = "https://elite-emporium.onrender.com";
window.addEventListener('load', function () 
{
    const admin=document.getElementById('superstatus');
    const campusSelect = document.getElementById('campus2');
    campusSelect.addEventListener('change', function() {
        const banner = document.getElementById('banner-name').textContent;
        if (admin.checked && banner === "Inventory") {
            inventoryRequest();
        }
    });
});
function inventoryRequest()
{
    let campus = document.getElementById("campus-name").textContent;
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const temp=document.getElementById('campus2').value;
        document.getElementById('campus-name').textContent=temp;
        campus=temp;
    }
    fetch(`${API_URL}/inventory_request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ campus })
    })
    .then(response => response.json())
    .then(data => {
        const inventory = data.inventory || [];
        const lowstock = data.lowstock || [];
        updateInventory(inventory,lowstock);
    })
    .catch(err => console.error("Products request failed:", err));
}
function updateInventory(inventory,lowstock)
{
    const container = document.getElementById("inventory_container");
    container.innerHTML = "";

    inventory.forEach(inventory => {
        const inventoryStr = JSON.stringify(inventory).replace(/'/g, "&apos;");
        container.innerHTML += `
            <div class="data">
          <div style="align-items: center; display: flex;">
            <img style="width: 140px; height: 110px; margin-right: 10px;" src="{{ url_for('static', filename='images/placeholder1.jpg') }}">
            <span>${ inventory.name }</span>
          </div>
          <div>${ inventory.id }</div>
          <div>${ inventory.spa_quantity }</div>
          <div>${ inventory.campus_quantity }</div>
          <div class="buttons">
            <div class="button" onclick="overlay('transfer')">Transfer</div>
            <div class="button" onclick="overlay('add')">Add</div>
            <div class="button" onclick="overlay('delete'); deleteID('${inventory.id}')">Delete</div>
          </div>
        </div>
        `;
    });
    const containers = document.getElementById("lowstock_container");
    containers.innerHTML = "";

    lowstock.forEach(lowstock => {
        const lowstockStr = JSON.stringify(lowstock).replace(/'/g, "&apos;");
        containers.innerHTML += `
            <div class="data">
          <div style="justify-content: center; display: flex;">${ lowstock.name }</div>
          <div class="notice">Low Stock</div>
        </div>
        `;
    });
}