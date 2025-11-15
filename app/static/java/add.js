selectedProduct= null;
function addProduct()
{
    document.getElementById('filter-order').style.display='none';
    document.getElementById('filter-search').style.display='none';
    document.getElementById('content').style.display='none';
    document.getElementById('add_product').style.display='flex';
    document.getElementById('banner-name').textContent='Add Product';
    document.getElementById('product-banner').textContent='Add Product';
    document.getElementById('product-button').textContent='Add';
    document.getElementById('product-upload').style.display='flex';
    const name = document.getElementById('addName');
    const description = document.getElementById('addDescription');
    const price = document.getElementById('addPrice');
    const sku = document.getElementById('addSKU');
    const category = document.getElementById('addCategory');
    name.value = '';
    description.value = '';
    price.value = '';
    sku.value = '';
    category.value = '';
    selectedProduct = null;
}
function editProduct(product)
{
    document.getElementById('filter-order').style.display='none';
    document.getElementById('filter-search').style.display='none';
    document.getElementById('content').style.display='none';
    document.getElementById('add_product').style.display='flex';
    document.getElementById('banner-name').textContent='Edit Product';
    document.getElementById('product-banner').textContent='Edit Product';
    document.getElementById('product-button').textContent='Save';
    document.getElementById('product-upload').style.display='none';
    const name = document.getElementById('addName');
    const description = document.getElementById('addDescription');
    const price = document.getElementById('addPrice');
    const sku = document.getElementById('addSKU');
    const category = document.getElementById('addCategory');
    name.value = product.name || '';
    description.value = product.description || '';
    price.value = product.price || '';
    sku.value = product.sku || '';
    category.value = product.category || '';
    selectedProduct=product;
}
function saveProduct() {
    const name = document.getElementById('addName').value.trim();
    const description = document.getElementById('addDescription').value.trim();
    const priceStr = document.getElementById('addPrice').value.trim();
    const sku = document.getElementById('addSKU').value.trim();
    const category = document.getElementById('addCategory').value.trim();
    const status = document.getElementById('product-banner').textContent;

    if (name === "") { alert("Please input the name!"); return; }
    if (description === "") { alert("Please input the description!"); return; }
    if (priceStr === "") { alert("Please input a valid price!"); return; }
    if (sku === "") { alert("Please input the SKU!"); return; }
    if (category === "") { alert("Please input the category!"); return; }

    const price = parseFloat(priceStr);
    if (isNaN(price)) {
        alert("Please input a valid numeric price!");
        return;
    }

    if (status === 'Edit Product') {
        const updatedFields = {};
        if (selectedProduct) {
            updatedFields.name = name;
            updatedFields.description = description;
            updatedFields.price = price;  // ✅ correctly parsed float
            updatedFields.category = category;
            updatedFields.id = selectedProduct.id;

            fetch("/update_product", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(updatedFields)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Product updated successfully!");
                    section('Dashboard');
                } else {
                    alert("Error updating product: " + data.message);
                }
            })
            .catch(err => console.error("Error:", err));
        }
    } else {
        // Handle Add Product here
    }
}
