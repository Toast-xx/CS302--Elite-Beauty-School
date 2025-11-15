window.addEventListener('load', function () {
    // Determine which search bar is present and which section is active
    const banner = document.getElementById('banner-name') ? document.getElementById('banner-name').value : '';
    const campusElem = document.getElementById('campus-name');
    const campus = campusElem ? campusElem.value : 'All';
    const adminElem = document.getElementById('superstatus');
    const isAdmin = adminElem && adminElem.checked;

    // User search bar logic (Users section)
    const userInput = document.getElementById('userSearchInput') || document.getElementById('searchBar');
    const userGoBtn = document.getElementById('userSearchGo');
    const userListContainer = document.querySelector('.section.users .listed .containers');
    const userResultsList = document.getElementById('search-result');

    function performUserSearch() {
        const query = userInput.value.trim();
        let campusValue = campus;
        if (isAdmin) campusValue = "All";
        if (query.length > 0) {
            fetch(`/search_users?q=${encodeURIComponent(query)}&campus=${encodeURIComponent(campusValue)}`)
                .then(response => response.json())
                .then(userlist => {
                    // If using a table/list container, update it
                    if (userListContainer) {
                        userListContainer.innerHTML = '';
                        userlist.forEach(user => {
                            const row = document.createElement('div');
                            row.className = 'data';
                            row.innerHTML = `
                                <div style="align-items: center; display: flex;">
                                    <span>${user.name}</span>
                                </div>
                                <div>${user.email}</div>
                                <div>${user.campus_name || 'N/A'}</div>
                                <div>${user.role || 'User'}</div>
                                <div><span style="color:green;">Active</span></div>
                                <div>
                                    <button class="btn btn-sm btn-secondary"
                                        onclick="editUser('${user.id}', '${user.name}', '${user.email}', '${user.campus_id}', '${user.clearance_level}', '', '', 1)">
                                        Edit
                                    </button>
                                </div>
                            `;
                            userListContainer.appendChild(row);
                        });
                    }
                    // If using a dropdown list, update it
                    if (userResultsList) {
                        userResultsList.innerHTML = '';
                        userlist.forEach(user => {
                            const li = document.createElement('li');
                            li.textContent = user.name;
                            li.addEventListener('click', () => {
                                window.location.href = `/user/${user.id}`;
                            });
                            userResultsList.appendChild(li);
                        });
                        userResultsList.style.display = userlist.length > 0 ? 'block' : 'none';
                    }
                })
                .catch(error => {
                    console.error('Error fetching user search results:', error);
                    if (userResultsList) userResultsList.style.display = 'none';
                });
        } else {
            if (userListContainer) userListContainer.innerHTML = '';
            if (userResultsList) {
                userResultsList.innerHTML = '';
                userResultsList.style.display = 'none';
            }
        }
    }

    // Product search bar logic (top banner or product section)
    const productInput = document.getElementById('productSearchInput') || document.getElementById('searchBar');
    const productResults = document.getElementById('product-search-result') || document.getElementById('search-result');

    function performProductSearch() {
        const query = productInput.value.trim();
        let campusValue = campus;
        if (isAdmin) campusValue = "All";
        if (query.length > 0) {
            fetch(`/search_products?q=${encodeURIComponent(query)}&campus=${encodeURIComponent(campusValue)}`)
                .then(response => response.json())
                .then(productList => {
                    productResults.innerHTML = '';
                    productList.forEach(product => {
                        const li = document.createElement('li');
                        li.textContent = product.name;
                        li.addEventListener('click', () => {
                            window.location.href = `/product/${product.id}`;
                        });
                        productResults.appendChild(li);
                    });
                    productResults.style.display = productList.length > 0 ? 'block' : 'none';
                })
                .catch(error => {
                    console.error('Error fetching product search results:', error);
                    productResults.style.display = 'none';
                });
        } else {
            productResults.innerHTML = '';
            productResults.style.display = 'none';
        }
    }

    // Attach event listeners based on which section is active
    if (banner === 'Users') {
        if (userInput && userResultsList) {
            userInput.addEventListener('input', performUserSearch);
        }
        if (userGoBtn) {
            userGoBtn.addEventListener('click', function (event) {
                event.preventDefault();
                performUserSearch();
            });
        }
    } else {
        if (productInput && productResults) {
            productInput.addEventListener('input', performProductSearch);
        }
    }
});