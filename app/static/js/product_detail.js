// Handles product image gallery switching and quantity controls on the product detail page.
// - Clicking a gallery thumbnail updates the main product image.
// - Plus/minus buttons adjust the quantity input, minimum value is 1.
// Ensure element IDs and classes match those in product_detail.html.

document.addEventListener('DOMContentLoaded', function () {
    const mainImg = document.getElementById('mainProductImg');
    const thumbs = document.querySelectorAll('.product-gallery-img');
    thumbs.forEach(function (thumb) {
        thumb.addEventListener('click', function () {
            mainImg.src = this.getAttribute('data-img');
        });
    });

    // Quantity increment/decrement
    const qtyInput = document.getElementById('qty-input');
    const minusBtn = document.getElementById('qty-minus');
    const plusBtn = document.getElementById('qty-plus');

    minusBtn.addEventListener('click', function () {
        let qty = parseInt(qtyInput.value, 10);
        if (qty > 1) {
            qtyInput.value = qty - 1;
        }
    });

    plusBtn.addEventListener('click', function () {
        let qty = parseInt(qtyInput.value, 10);
        qtyInput.value = qty + 1;
    });
});