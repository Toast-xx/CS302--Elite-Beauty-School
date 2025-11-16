
window.addEventListener('load', function () {

  const searchInput = document.getElementById('searchBar');
  const resultsList = document.getElementById('search-result');

  if (searchInput && resultsList) {

    searchInput.addEventListener('input', function() {
      const banner = document.getElementById('banner-name').textContent.trim();

      const query = this.value.trim();
      let campus = document.getElementById("campus-name").textContent;
      const admin = document.getElementById('superstatus');

      if (admin.checked) {
        campus = "All";
      }

      if (query.length === 0) {
        resultsList.innerHTML = '';
        resultsList.style.display = 'none';
        return;
      }
      if (banner === 'Users') {
        fetch(`${API_URL}/search_users?q=${encodeURIComponent(query)}&campus=${encodeURIComponent(campus)}`)
          .then(res => res.json())
          .then(users => {
            resultsList.innerHTML = '';
            users.forEach(user => {
              const li = document.createElement('li');
              li.textContent = user.name;
              li.addEventListener('click', () => {
                searchInput.value = '';
                resultsList.innerHTML = '';
                resultsList.style.display = 'none';
                ;
              });
              resultsList.appendChild(li);
            });
            resultsList.style.display = users.length > 0 ? 'block' : 'none';
          });
      }
      else {
        fetch(`${API_URL}/search_products?q=${encodeURIComponent(query)}&campus=${encodeURIComponent(campus)}`)
          .then(res => res.json())
          .then(products => {
            resultsList.innerHTML = '';
            products.forEach(product => {
              const li = document.createElement('li');
              li.textContent = product.name;
              li.addEventListener('click', () => {
                searchInput.value = '';
                resultsList.innerHTML = '';
                resultsList.style.display = 'none';
                editProduct(product);
              });
              resultsList.appendChild(li);
            });
            resultsList.style.display = products.length > 0 ? 'block' : 'none';
          });
      }

    });

  }
});
