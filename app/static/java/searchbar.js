window.addEventListener('DOMContentLoaded', function () {
    // Get elements for user search
    const userInput = document.getElementById('userSearchInput');
    const userGoBtn = document.getElementById('userSearchGo');
    const userResultsList = document.getElementById('user-search-result');
    const campusElem = document.getElementById('campus-name');
    const adminElem = document.getElementById('superstatus');
    const campus = campusElem ? campusElem.value : 'All';
    const isAdmin = adminElem && adminElem.checked;

    // Get elements for product search
    const productInput = document.getElementById('productSearchInput');
    const productGoBtn = document.querySelector('#product-search-bar button');
    const productResults = document.getElementById('product-search-result');

    // User search function
    function performUserSearch() {
        if (!userInput || !userResultsList) return;
        const query = userInput.value.trim();
        let campusValue = campus;
        if (isAdmin) campusValue = "All";
        if (!query) {
            userResultsList.innerHTML = '';
            userResultsList.style.display = 'none';
            return;
        }
        fetch(`/user/search?q=${encodeURIComponent(query)}&campus=${encodeURIComponent(campusValue)}`)
            .then(response => response.json())
            .then(userlist => {
                userResultsList.innerHTML = '';
                if (Array.isArray(userlist) && userlist.length > 0) {
                    userlist.forEach(user => {
                        const li = document.createElement('li');
                        li.textContent = `${user.name} (${user.email})`;
                        li.addEventListener('click', () => {
                            editUser(
                                user.id,
                                user.name,
                                user.email,
                                user.campus_id,
                                user.clearance_level,
                                user.start_date || '',
                                user.end_date || '',
                                user.active ? 1 : 0
                            );
                            userResultsList.style.display = 'none';
                        });
                        userResultsList.appendChild(li);
                    });
                    userResultsList.style.display = 'block';
                } else {
                    userResultsList.innerHTML = '<li>No users found.</li>';
                    userResultsList.style.display = 'block';
                }
            })
            .catch(error => {
                userResultsList.innerHTML = `<li>Error: ${error.message}</li>`;
                userResultsList.style.display = 'block';
            });
    }

    // Product search function
    function performProductSearch() {
        if (!productInput || !productResults) return;
        const query = productInput.value.trim();
        let campusValue = campus;
        if (isAdmin) campusValue = "All";
        if (!query) {
            productResults.innerHTML = '';
            productResults.style.display = 'none';
            return;
        }
        fetch(`/search_products?q=${encodeURIComponent(query)}&campus=${encodeURIComponent(campusValue)}`)
            .then(response => response.json())
            .then(productList => {
                productResults.innerHTML = '';
                if (Array.isArray(productList) && productList.length > 0) {
                    productList.forEach(product => {
                        const li = document.createElement('li');
                        li.textContent = product.name;
                        li.addEventListener('click', () => {
                            window.location.href = `/product/${product.id}`;
                        });
                        productResults.appendChild(li);
                    });
                    productResults.style.display = 'block';
                } else {
                    productResults.innerHTML = '<li>No products found.</li>';
                    productResults.style.display = 'block';
                }
            })
            .catch(error => {
                productResults.innerHTML = `<li>Error: ${error.message}</li>`;
                productResults.style.display = 'block';
            });
    }

    // Attach user search events
    if (userInput && userGoBtn && userResultsList) {
        userGoBtn.addEventListener('click', function (event) {
            event.preventDefault();
            performUserSearch();
        });
        userInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                performUserSearch();
            }
        });
        userInput.addEventListener('input', performUserSearch);
    }

    // Attach product search events
    if (productInput && productGoBtn && productResults) {
        productGoBtn.addEventListener('click', function (event) {
            event.preventDefault();
            performProductSearch();
        });
        productInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                performProductSearch();
            }
        });
        productInput.addEventListener('input', performProductSearch);
    }
});