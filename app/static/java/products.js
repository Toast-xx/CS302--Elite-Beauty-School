
window.addEventListener('load', function () 
{
    const admin=document.getElementById('superstatus');
    const campusSelect = document.getElementById('campus2');
    campusSelect.addEventListener('change', function() {
        const banner = document.getElementById('banner-name').textContent;
        if (admin.checked && banner === "Products") {
            productsRequest();
        }
    });
});
function productsRequest()
{
    let campus = document.getElementById("campus-name").textContent;
    const admin=document.getElementById('superstatus');
    if(admin.checked)
    {
        const temp=document.getElementById('campus2').value;
        document.getElementById('campus-name').textContent=temp;
        campus=temp;
    }
    fetch(`${API_URL}/products_request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ campus })
    })
    .then(response => response.json())
    .then(data => {
        const products = data.products || [];
        updateProducts(products);
    })
    .catch(err => console.error("Products request failed:", err));
}
function updateProducts(data)
{
    const container = document.getElementById("products_container");
    container.innerHTML = "";

    data.forEach(product => {
        const productStr = JSON.stringify(product).replace(/'/g, "&apos;");
        let imgSrc = "/static/images/placeholder1.jpg";
        if (product.image_gallery && product.image_gallery.length > 0) {
            if (product.image_gallery[0].startsWith("http")) {
                imgSrc = product.image_gallery[0];
            } else {
                imgSrc = `/admin/uploaded_images/${product.image_gallery[0]}`;
            }
        }
       container.innerHTML += `
            <div class="data">
                <img style="width: 140px; height: 110px;"
                     src="${imgSrc}" alt="${product.name}">

                <div>${product.name}</div>
                <div>$${product.price}</div>
                <div>${product.campus}</div>

                <div class="buttons">
                    <div class="edit" onclick='editProduct(${productStr})'>Edit</div>
                    <div class="delete" onclick="overlay('delete'); deleteID('${product.id}')">Delete</div>
                </div>
            </div>
        `;
    });
}