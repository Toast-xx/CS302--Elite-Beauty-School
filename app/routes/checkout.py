# Handles the checkout process for the cart.
# Integrates Stripe for payment processing and renders the checkout page.
# Requires user authentication and uses cart data from get_or_create_cart.
# Stripe expects the total amount in cents (NZD).
# Ensure STRIPE_API_KEY and STRIPE_PUBLIC_KEY are set in your environment.

from flask import render_template, redirect, url_for, request
from flask_login import current_user
from decimal import Decimal
from app.routes.cart import get_or_create_cart, cart_bp
import stripe
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set Stripe secret key for backend operations
stripe.api_key = os.getenv("STRIPE_API_KEY")

@cart_bp.route('/cart/checkout', methods=['GET', 'POST'])
def checkout():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    cart = get_or_create_cart()
    cart_items = cart.items if cart else []
    subtotal = sum(item.campus_product.price * item.quantity for item in cart_items)
    shipping = Decimal("5.00")
    total = int((subtotal + shipping) * 100)  # Stripe expects cents

    if request.method == 'POST':
        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'nzd',
                        'product_data': {
                            'name': 'Campus Cart Order',
                        },
                        'unit_amount': total,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('cart.complete_order', _external=True),
            cancel_url=url_for('cart.checkout', _external=True) + '?canceled=true',
        )
        return redirect(session.url, code=303)

    # Pass Stripe public key to frontend for Stripe.js
    return render_template(
        'checkout.html',
        cart_items=cart_items,
        subtotal=subtotal,
        shipping=shipping,
        total=subtotal + shipping,
        stripe_api_key=os.getenv("STRIPE_API_KEY")
    )
