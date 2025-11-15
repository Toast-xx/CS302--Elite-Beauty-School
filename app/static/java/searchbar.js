window.addEventListener('load', function() {
  const searchInput = document.getElementById('searchBar');
  const resultsList = document.getElementById('search-result');
  const banner=document.getElementById('banner-name').value;
  if(banner==='Users')
  {
    if (searchInput && resultsList) {
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        const campus = document.getElementById("campus-name").value;
        const admin=document.getElementById('superstatus');
        if(admin.checked)
        {
            campus="All";
        }
        if (query.length > 0) {
            fetch(`/search_users?q=${encodeURIComponent(query)}&campus=${encodeURIComponent(campus)}`)
                .then(response => response.json())
                .then(userlist => {
                    resultsList.innerHTML = '';
                    userlist.forEach(user => {
                        const li = document.createElement('li');
                        li.textContent = user.name;
                        li.addEventListener('click', () => {
                            window.location.href = `/user/${user.id}`;
                        });
                        resultsList.appendChild(li);
                    });
                    resultsList.style.display = userlist.length > 0 ? 'block' : 'none';
                })
                .catch(error => {
                    console.error('Error fetching search results:', error);
                    resultsList.style.display = 'none';
                });
        } else {
            resultsList.innerHTML = '';
            resultsList.style.display = 'none';
        }
    });
  }

  }
  else
  {
    if (searchInput && resultsList) {
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        const campus = document.getElementById("campus-name").value;
        const admin=document.getElementById('superstatus');
        if(admin.checked)
        {
            campus="All";
        }
        if (query.length > 0) {
            fetch(`/search_products?q=${encodeURIComponent(query)}&campus=${encodeURIComponent(campus)}`)
                .then(response => response.json())
                .then(productList => {
                    resultsList.innerHTML = '';
                    productList.forEach(product => {
                        const li = document.createElement('li');
                        li.textContent = product.name;
                        li.addEventListener('click', () => {
                            window.location.href = `/product/${product.id}`;
                        });
                        resultsList.appendChild(li);
                    });
                    resultsList.style.display = productList.length > 0 ? 'block' : 'none';
                })
                .catch(error => {
                    console.error('Error fetching search results:', error);
                    resultsList.style.display = 'none';
                });
        } else {
            resultsList.innerHTML = '';
            resultsList.style.display = 'none';
        }
    });
  }
  }
});