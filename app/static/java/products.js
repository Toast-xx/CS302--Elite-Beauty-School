window.addEventListener('load', function() 
{
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const campusSelect = document.getElementById('campus2');
        const banner=document.getElementById('banner-name').value;
        if(banner==="Products")
        {
            campusSelect.addEventListener('change', function() {
                productsRequest();
            });
        }
    }
});
function productsRequest()
{
    const campus = document.getElementById("campus-name").value;
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const temp=document.getElementById('campus2').value;
        document.getElementById('campus-name').value=temp;
        campus=temp;
    }
    fetch("/products_request", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ campus })
    })
    .then(response => response.json())
    .then(data => {
        updateProducts(data);
    })
    .catch(err => console.error("Products request failed:", err));
}
function updateProducts(data)
{
    const container = document.getElementById("products_container");
    container.innerHTML = "";

    data.forEach(product => {
        container.innerHTML += `
            <div class="data">
                <img style="width: 140px; height: 110px;"
                     src="/static/images/placeholder1.jpg">

                <div>${product.name}</div>
                <div>${product.price}%</div>
                <div>${product.campus}</div>

                <div class="buttons">
                    <div class="edit" onclick="editProduct('${product.id}')">Edit</div>
                    <div class="delete" onclick="overlay('delete'); deleteID('${product.id}')">Delete</div>
                </div>
            </div>
        `;
    });
}
function deleteID(id)
{
    const target=document.getElementById('deleteID');
    target.value=id;
}