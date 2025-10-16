function updateShipping(amount) {
    // Update shipping cost display in both places
    document.getElementById('shipping-cost').textContent = amount === 0 ? 'Free' : '$' + amount.toFixed(2);
    document.getElementById('shipping-summary').textContent = amount === 0 ? 'Free' : '$' + amount.toFixed(2);

    // Get subtotal from the page (parse as float)
    var subtotal = parseFloat(document.getElementById('subtotal-cost').textContent.replace('$', ''));
    var total = subtotal + amount;

    // Update total display
    document.getElementById('total-cost').textContent = '$' + total.toFixed(2);
}

function updateQty(productId, delta) {
    // delta > 0 -> use existing add_to_cart route which increments by 1
    if (delta > 0) {
        window.location.href = '/add_to_cart/' + productId;
        return;
    }

    // delta < 0 -> use existing remove_from_cart route (note: current backend removes the item entirely).
    // If you want "decrement quantity" instead of full removal, add a backend route to decrement quantity.
    if (delta < 0) {
        window.location.href = '/remove_from_cart/' + productId;
    }
}

function removeFromCart(productId) {
    window.location.href = '/remove_from_cart/' + productId;
}

// Attach event handlers so we don't use inline JS (prevents VS/TS parser warnings on Jinja templates).
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.qty-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var pid = this.dataset.productId;
            var delta = parseInt(this.dataset.delta, 10);
            if (pid) updateQty(pid, delta);
        });
    });

    document.querySelectorAll('.cart-item-remove').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var pid = this.dataset.productId;
            if (pid) removeFromCart(pid);
        });
    });
});