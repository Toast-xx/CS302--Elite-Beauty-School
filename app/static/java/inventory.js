
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
        let imgSrc = "/static/images/placeholder1.jpg";
        if (item.image_gallery && item.image_gallery.length > 0) {
            if (item.image_gallery[0].startsWith("http")) {
                imgSrc = item.image_gallery[0];
            } else {
                imgSrc = `/admin/uploaded_image/${item.image_gallery[0]}`;
            }
        }
        container.innerHTML += `
            <div class="data">
          <div style="align-items: center; display: flex;">
            <img style="width: 140px; height: 110px; margin-right: 10px;" src="${imgSrc}" alt="${item.name}">
            <span>${ inventory.name }</span>
          </div>
          <div>${ inventory.id }</div>
          <div>${item.campus ? item.campus : ''}</div>
          <div>${ inventory.spa_quantity }</div>
          <div>${ inventory.campus_quantity }</div>
          <div class="buttons">
            <div class="button" onclick="overlay('transfer')">Transfer</div>
            <div class="button" onclick="overlay('add'); addId('${inventory.id}')">Add</div>
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