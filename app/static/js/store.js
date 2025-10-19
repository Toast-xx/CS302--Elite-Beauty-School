// Handles AJAX-based product filtering and search on the store page.
// Intercepts form submissions and input changes to update the product list dynamically
// without a full page reload. Expects a <form> for filters/search and a .product-list
// container for rendering results.

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const productListContainer = document.querySelector('.product-list');

    // Intercept form submission (button click or Enter)
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const params = new URLSearchParams(new FormData(form));
        params.append('ajax', '1');
        fetch(`/store/?${params.toString()}`)
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
        fetch(`/store/?${params.toString()}`)
            .then(response => response.text())
            .then(html => {
                productListContainer.innerHTML = html;
            });
    });
});