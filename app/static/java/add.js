function addProduct()
{
    document.getElementById('filter-order').style.display='none';
    document.getElementById('filter-search').style.display='none';
    document.getElementById('content').style.display='none';
    document.getElementById('add_product').style.display='flex';
    document.getElementById('banner-name').textContent='Add Product';
}
function saveProduct()
{
    const name=document.getElementById('addName');
    const description=document.getElementById('addDescription');
    const price=document.getElementById('addPrice');
    const sku=document.getElementById('addSKU');
    const category=document.getElementById('addCategory');
    if(name.value.trim()==="")
    {
        alert("Please input the name!");
        return;
    }
    if(description.value.trim()==="")
    {
        alert("Please input the description!");
        return;
    }
    if(price.value.trim()==="")
    {
        alert("Please input a valid price!");
        return;
    }
    if(sku.value.trim()==="")
    {
        alert("Please input the SKU!");
        return;
    }
    if(category.value.trim()==="")
    {
        alert("Please input the category!");
        return;
    }
}