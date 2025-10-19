// Handles cart interactions on the cart page, including updating quantities, removing items, 
// recalculating totals, and updating shipping cost. Relies on specific HTML element IDs and classes 
// in cart.html for dynamic updates. All AJAX requests expect Flask endpoints for cart operations.

function updateShipping(amount) {
    // Updates shipping cost and recalculates total
    document.getElementById('shipping-cost').textContent = amount === 0 ? 'Free' : '$' + amount.toFixed(2);
    document.getElementById('shipping-summary').textContent = amount === 0 ? 'Free' : '$' + amount.toFixed(2);

    // Get subtotal from the page (parse as float)
    var subtotal = parseFloat(document.getElementById('subtotal-cost').textContent.replace('$', ''));
    var total = subtotal + amount;

    // Update total display
    document.getElementById('total-cost').textContent = '$' + total.toFixed(2);
}

function updateQty(productId, delta) {
    // Sends AJAX request to update quantity of a cart item
    fetch(`/cart/update_quantity/${productId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ change: delta })
    })
        .then(response => response.json())
        .then(data => {
            if (data.new_quantity !== undefined) {
                document.getElementById(`quantity-${productId}`).textContent = data.new_quantity;
                document.getElementById(`cost-${productId}`).textContent = data.cost.toFixed(2);
                updateCartSummary();
            } else {
                alert('Error updating quantity');
            }
        });
}

function removeFromCart(productId) {
    // Sends AJAX request to remove an item from the cart
    fetch(`/cart/delete_item/${productId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`cart-item-${productId}`).remove();
                updateCartSummary();
            } else {
                alert('Error deleting item');
            }
        });
}

function updateCartSummary() {
    // Recalculates and updates subtotal and total after changes
    let subtotal = 0;
    document.querySelectorAll('.cart-item-cost span').forEach(function (costSpan) {
        subtotal += parseFloat(costSpan.textContent);
    });

    document.getElementById('subtotal-cost').textContent = '$' + subtotal.toFixed(2);

    // Get shipping cost from the summary (parse as float, fallback to 5.00)
    let shippingText = document.getElementById('shipping-summary').textContent;
    let shipping = shippingText === 'Free' ? 0 : parseFloat(shippingText.replace('$', '')) || 5.00;

    let total = subtotal + shipping;
    document.getElementById('total-cost').textContent = '$' + total.toFixed(2);
}

// Attach event listeners for quantity and remove buttons after DOM is loaded
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