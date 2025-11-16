
selectedProduct = null;

// --- Image upload logic START ---
let selectedImages = [];

const addImagesInput = document.getElementById('addImagesInput');
if (addImagesInput) {
    addImagesInput.addEventListener('change', function (event) {
        // Append new files to selectedImages, avoiding duplicates by name
        const newFiles = Array.from(event.target.files);
        const existingNames = selectedImages.map(f => f.name);
        newFiles.forEach(file => {
            if (!existingNames.includes(file.name)) {
                selectedImages.push(file);
            }
        });

        const preview = document.getElementById('imagePreview');
        if (preview) {
            preview.innerHTML = '';
            if (selectedImages.length > 0) {
                // Show a message about how many images were selected
                const info = document.createElement('div');
                info.textContent = `${selectedImages.length} image(s) selected.`;
                info.style.marginBottom = '10px';
                info.style.color = '#2d7a2d';
                preview.appendChild(info);
            }
            selectedImages.forEach(file => {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.style.maxWidth = '100px';
                    img.style.margin = '5px';
                    preview.appendChild(img);
                };
                reader.readAsDataURL(file);
            });
        }
    });
}
// --- Image upload logic END ---

function addProduct() {
    document.getElementById('filter-order').style.display = 'none';
    document.getElementById('filter-search').style.display = 'none';
    document.getElementById('content').style.display = 'none';
    document.getElementById('add_product').style.display = 'flex';
    document.getElementById('banner-name').textContent = 'Add Product';
    document.getElementById('product-banner').textContent = 'Add Product';
    document.getElementById('product-button').textContent = 'Add';
    document.getElementById('product-upload').style.display = 'flex';
    const name = document.getElementById('addName');
    const description = document.getElementById('addDescription');
    const price = document.getElementById('addPrice');
    const brand = document.getElementById('addBrand');
    const categorySelect = document.getElementById('addCategorySelect');
    const subCategorySelect = document.getElementById('addSubCategorySelect');
    name.value = '';
    description.value = '';
    price.value = '';
    if (brand) brand.value = '';
    if (categorySelect) categorySelect.selectedIndex = 0;
    if (subCategorySelect) subCategorySelect.selectedIndex = 0;
    selectedProduct = null;
    // Reset image selection and preview
    selectedImages = [];
    if (addImagesInput) addImagesInput.value = '';
    const preview = document.getElementById('imagePreview');
    if (preview) preview.innerHTML = '';
    // Fetch categories/subcategories for dropdowns
    fetchCategoriesAndSubCategories();
}

function editProduct(product) {
    document.getElementById('filter-order').style.display = 'none';
    document.getElementById('filter-search').style.display = 'none';
    document.getElementById('content').style.display = 'none';
    document.getElementById('add_product').style.display = 'flex';
    document.getElementById('banner-name').textContent = 'Edit Product';
    document.getElementById('product-banner').textContent = 'Edit Product';
    document.getElementById('product-button').textContent = 'Save';
    document.getElementById('product-upload').style.display = 'none';
    const name = document.getElementById('addName');
    const description = document.getElementById('addDescription');
    const price = document.getElementById('addPrice');
    const brand = document.getElementById('addBrand');
    const categorySelect = document.getElementById('addCategorySelect');
    const subCategorySelect = document.getElementById('addSubCategorySelect');
    name.value = product.name || '';
    description.value = product.description || '';
    price.value = product.price || '';
    if (brand) brand.value = product.brand || '';
    if (categorySelect) categorySelect.value = product.category_id || '';
    if (subCategorySelect) subCategorySelect.value = product.sub_category_id || '';
    selectedProduct = product;
    // Hide image upload for edit, clear preview
    if (addImagesInput) addImagesInput.value = '';
    const preview = document.getElementById('imagePreview');
    if (preview) preview.innerHTML = '';
    // Fetch categories/subcategories for dropdowns
    fetchCategoriesAndSubCategories();
}

function saveProduct() {
    const name = document.getElementById('addName').value.trim();
    const description = document.getElementById('addDescription').value.trim();
    const priceStr = document.getElementById('addPrice').value.trim();
    const brand = document.getElementById('addBrand') ? document.getElementById('addBrand').value.trim() : '';
    const categorySelect = document.getElementById('addCategorySelect');
    const subCategorySelect = document.getElementById('addSubCategorySelect');
    const categoryId = categorySelect ? categorySelect.value : '';
    const subCategoryId = subCategorySelect ? subCategorySelect.value : '';
    const status = document.getElementById('product-banner').textContent;

    if (name === "") { alert("Please input the name!"); return; }
    if (description === "") { alert("Please input the description!"); return; }
    if (priceStr === "") { alert("Please input a valid price!"); return; }
    if (categoryId === "" || categoryId === "add_new") { alert("Please select a category!"); return; }
    if (subCategoryId === "" || subCategoryId === "add_new") { alert("Please select a sub-category!"); return; }

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
            updatedFields.price = price;
            updatedFields.brand = brand;
            updatedFields.category_id = categoryId;
            updatedFields.sub_category_id = subCategoryId;
            updatedFields.id = selectedProduct.id;

            fetch(`${API_URL}/update_product`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include", // <-- add this line
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
        // Handle Add Product with images
        const formData = new FormData();
        formData.append('name', name);
        formData.append('description', description);
        formData.append('price', price);
        formData.append('brand', brand);
        formData.append('category_id', categoryId);
        formData.append('sub_category_id', subCategoryId);
        selectedImages.forEach((file) => {
            formData.append('images', file);
        });

        fetch(`${API_URL}/add_product`, {
            method: "POST",
            credentials: "include",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let msg = "Product added successfully!";
                    if (data.images_saved !== undefined) {
                        msg += ` ${data.images_saved} image(s) uploaded.`;
                    }
                    alert(msg);
                    section('Dashboard');
                } else {
                    alert("Error adding product: " + data.message);
                }
            })
            .catch(err => console.error("Error:", err));
    }
}

// --- Category & Sub-category Dropdown Logic ---

let categories = [];
let subCategories = [];

function fetchCategoriesAndSubCategories() {
    fetch(`${API_URL}/get_categories_subcategories`)
        .then(res => res.json())
        .then(data => {
            categories = data.categories;
            subCategories = data.sub_categories;
            populateCategoryDropdown();
        });
}

function populateCategoryDropdown() {
    const categorySelect = document.getElementById('addCategorySelect');
    categorySelect.innerHTML = '';
    categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.id;
        option.textContent = cat.name;
        categorySelect.appendChild(option);
    });
    // Add "Add new" option
    const addNewOption = document.createElement('option');
    addNewOption.value = 'add_new';
    addNewOption.textContent = 'Add new category...';
    categorySelect.appendChild(addNewOption);

    categorySelect.onchange = onCategoryChange;
    populateSubCategoryDropdown();
}

function populateSubCategoryDropdown() {
    const categoryId = parseInt(document.getElementById('addCategorySelect').value);
    const subCategorySelect = document.getElementById('addSubCategorySelect');
    subCategorySelect.innerHTML = '';
    subCategories.filter(sc => sc.category_id === categoryId).forEach(sc => {
        const option = document.createElement('option');
        option.value = sc.id;
        option.textContent = sc.name;
        subCategorySelect.appendChild(option);
    });
    // Add "Add new" option
    const addNewOption = document.createElement('option');
    addNewOption.value = 'add_new';
    addNewOption.textContent = 'Add new sub-category...';
    subCategorySelect.appendChild(addNewOption);

    subCategorySelect.onchange = onSubCategoryChange;
}

function onCategoryChange() {
    const select = document.getElementById('addCategorySelect');
    if (select.value === 'add_new') {
        document.getElementById('newCategoryInput').style.display = 'inline';
        document.getElementById('addCategoryBtn').style.display = 'inline';
    } else {
        document.getElementById('newCategoryInput').style.display = 'none';
        document.getElementById('addCategoryBtn').style.display = 'none';
        populateSubCategoryDropdown();
    }
}

function onSubCategoryChange() {
    const select = document.getElementById('addSubCategorySelect');
    if (select.value === 'add_new') {
        document.getElementById('newSubCategoryInput').style.display = 'inline';
        document.getElementById('addSubCategoryBtn').style.display = 'inline';
    } else {
        document.getElementById('newSubCategoryInput').style.display = 'none';
        document.getElementById('addSubCategoryBtn').style.display = 'none';
    }
}

function addCategory() {
    const name = document.getElementById('newCategoryInput').value.trim();
    if (!name) return alert("Enter a category name.");
    fetch(`${API_URL}/admin/add_category`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: "include",
        body: JSON.stringify({ name })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Category added!");
                document.getElementById('newCategoryInput').value = '';
                document.getElementById('newCategoryInput').style.display = 'none';
                document.getElementById('addCategoryBtn').style.display = 'none';
                fetchCategoriesAndSubCategories();
            } else {
                alert(data.message || "Error adding category.");
            }
        });
}

function addSubCategory() {
    const name = document.getElementById('newSubCategoryInput').value.trim();
    const categoryId = document.getElementById('addCategorySelect').value;
    if (!name || !categoryId || categoryId === 'add_new') return alert("Select category and enter sub-category name.");
    fetch(`${API_URL}/admin/add_subcategory`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: "include",
        body: JSON.stringify({ name, category_id: categoryId })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Sub-category added!");
                document.getElementById('newSubCategoryInput').value = '';
                document.getElementById('newSubCategoryInput').style.display = 'none';
                document.getElementById('addSubCategoryBtn').style.display = 'none';
                fetchCategoriesAndSubCategories();
            } else {
                alert(data.message || "Error adding sub-category.");
            }
        });
}

// --- Call this when the add product form is shown ---
window.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('addCategorySelect')) {
        fetchCategoriesAndSubCategories();
    }
});