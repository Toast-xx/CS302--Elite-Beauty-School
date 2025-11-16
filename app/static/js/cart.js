
// - Handles cart item quantity updates, item removal, and summary recalculation via AJAX.
// - Updates shipping and total cost dynamically on the cart page.
// - Integrates with Flask backend endpoints for cart operations.
// - Attaches event listeners to quantity and remove buttons for interactive cart management.

const API_URL = "https://elite-emporium.onrender.com";
function updateQty(campusProductId, delta) {
    // Send AJAX request to update item quantity in the cart
    fetch(`${API_URL}/cart/update_quantity/${campusProductId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ change: delta })
    })
        .then(response => response.json())
        .then(data => {
            if (data.new_quantity !== undefined) {
                document.getElementById(`quantity-${campusProductId}`).textContent = data.new_quantity;
                document.getElementById(`cost-${campusProductId}`).textContent = data.cost.toFixed(2);
                updateCartSummary();
            } else {
                alert('Error updating quantity');
            }
        });
}

function removeFromCart(campusProductId) {
    // Send AJAX request to remove item from the cart
    fetch(`${API_URL}/cart/delete_item/${campusProductId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`cart-item-${campusProductId}`).remove();
                updateCartSummary();
            } else {
                alert('Error deleting item');
            }
        });
}

function updateCartSummary() {
    // Recalculate and update subtotal, shipping, and total cost
    let subtotal = 0;
    document.querySelectorAll('.cart-item-cost span').forEach(function (costSpan) {
        subtotal += parseFloat(costSpan.textContent);
    });

    document.getElementById('subtotal-cost').textContent = '$' + subtotal.toFixed(2);

    let shippingText = document.getElementById('shipping-summary').textContent;
    let shipping = shippingText === 'Free' ? 0 : parseFloat(shippingText.replace('$', '')) || 5.00;

    let total = subtotal + shipping;
    document.getElementById('total-cost').textContent = '$' + total.toFixed(2);
}

document.addEventListener('DOMContentLoaded', function () {
    // Attach event listeners to quantity buttons
    document.querySelectorAll('.qty-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent form submission if inside a form
            var campusProductId = this.dataset.campusProductId;
            var delta = parseInt(this.dataset.delta, 10);
            if (campusProductId) updateQty(campusProductId, delta);
        });
    });

    // Attach event listeners to remove buttons
    document.querySelectorAll('.cart-item-remove').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent form submission if inside a form
            var campusProductId = this.dataset.campusProductId;
            if (campusProductId) removeFromCart(campusProductId);
        });
    });
});