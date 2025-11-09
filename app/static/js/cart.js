function updateShipping(amount) {
    document.getElementById('shipping-cost').textContent = amount === 0 ? 'Free' : '$' + amount.toFixed(2);
    document.getElementById('shipping-summary').textContent = amount === 0 ? 'Free' : '$' + amount.toFixed(2);

    var subtotal = parseFloat(document.getElementById('subtotal-cost').textContent.replace('$', ''));
    var total = subtotal + amount;
    document.getElementById('total-cost').textContent = '$' + total.toFixed(2);
}

function updateQty(campusProductId, delta) {
    fetch(`/cart/update_quantity/${campusProductId}`, {
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
    fetch(`/cart/delete_item/${campusProductId}`, {
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
    document.querySelectorAll('.qty-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent form submission if inside a form
            var campusProductId = this.dataset.campusProductId;
            var delta = parseInt(this.dataset.delta, 10);
            if (campusProductId) updateQty(campusProductId, delta);
        });
    });

    document.querySelectorAll('.cart-item-remove').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent form submission if inside a form
            var campusProductId = this.dataset.campusProductId;
            if (campusProductId) removeFromCart(campusProductId);
        });
    });
});