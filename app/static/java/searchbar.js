window.addEventListener('load', function () {
    // Product/global search bar logic (top banner)
    const productInput = document.getElementById('productSearchInput');
    const productResults = document.getElementById('product-search-result');
    if (productInput && productResults) {
        productInput.addEventListener('input', function () {
            const query = this.value.trim();
            if (query.length > 0) {
                fetch(`/searchProduct?q=${encodeURIComponent(query)}`)
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
        });
    }

    // User search bar logic (Users section)
    const userInput = document.getElementById('userSearchInput');
    const userGoBtn = document.getElementById('userSearchGo');
    const userListContainer = document.querySelector('.section.users .listed .containers'); // User list table body

    function performUserSearch() {
        const query = userInput.value.trim();
        if (query.length > 0) {
            fetch(`/searchAdmin?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(userlist => {
                    // Update user list table
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
                })
                .catch(error => {
                    console.error('Error fetching user search results:', error);
                });
        } else {
            // Optionally, reload all users or clear the table
        }
    }

    if (userInput && userGoBtn) {
        userGoBtn.addEventListener('click', function (event) {
            event.preventDefault();
            performUserSearch();
        });
        userInput.addEventListener('input', performUserSearch);
    }
});