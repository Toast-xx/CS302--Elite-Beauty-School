
// - Handles AJAX-based product filtering and dynamic search suggestions (autocomplete) for the store page.
// - Intercepts form submissions and filter changes to update product listings without page reloads.
// - Creates and manages an autocomplete dropdown for product search input.
// - Integrates with Flask backend endpoints for product filtering and search suggestions.
// - Attaches event listeners for instant filtering and search interactivity.
const API_URL = "https://elite-emporium.onrender.com";
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const productListContainer = document.querySelector('.product-list');
    const searchInput = document.querySelector('input[name="search"]');

    // Intercept form submission (button click or Enter)
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const params = new URLSearchParams(new FormData(form));
        params.append('ajax', '1');
        fetch(`${API_URL}/store/?${params.toString()}`)
        credentials: "include"
            .then(response => response.text())
            .then(html => {
                productListContainer.innerHTML = html;
            });
    });

    // Optionally, handle change events for instant filtering
    form.addEventListener('change', function (e) {
        e.preventDefault();
        const params = new URLSearchParams(new FormData(form));
        params.append('ajax', '1');
        fetch(`${API_URL}/store/?${params.toString()}`)
        credentials: "include"
            .then(response => response.text())
            .then(html => {
                productListContainer.innerHTML = html;
            });
    });

    // --- Autocomplete dropdown for product search ---
    // Create dropdown element
    let dropdown = document.createElement('div');
    dropdown.className = 'autocomplete-dropdown';
    dropdown.style.position = 'absolute';
    dropdown.style.zIndex = '1000';
    dropdown.style.background = '#fff';
    dropdown.style.border = '1px solid #ccc';
    dropdown.style.width = searchInput.offsetWidth + 'px';
    dropdown.style.display = 'none';
    searchInput.parentNode.appendChild(dropdown);

    // Position dropdown below the search input
    function positionDropdown() {
        const rect = searchInput.getBoundingClientRect();
        dropdown.style.left = rect.left + window.scrollX + 'px';
        dropdown.style.top = rect.bottom + window.scrollY + 'px';
        dropdown.style.width = rect.width + 'px';
    }

    // Fetch suggestions as user types
    searchInput.addEventListener('input', function () {
        const query = this.value;
        positionDropdown();
        if (query.length < 2) {
            dropdown.style.display = 'none';
            dropdown.innerHTML = '';
            return;
        }
        fetch(`${API_URL}/store/search_suggestions?q=${encodeURIComponent(query)}`)
        credentials: "include"
            .then(res => res.json())
            .then(data => {
                if (data.length === 0) {
                    dropdown.style.display = 'none';
                    dropdown.innerHTML = '';
                    return;
                }
                dropdown.innerHTML = data.map(item =>
                    `<a class="dropdown-item" href="/product/${item.id}" style="display:flex;align-items:center;">
                        ${item.image ? `<img src="${item.image}" style="width:24px;height:24px;margin-right:8px;">` : ''}
                        <span>${item.name}</span>
                    </a>`
                ).join('');
                dropdown.style.display = 'block';
            });
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', function (e) {
        if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });

    // Reposition dropdown on window resize/scroll
    window.addEventListener('resize', positionDropdown);
    window.addEventListener('scroll', positionDropdown);
});