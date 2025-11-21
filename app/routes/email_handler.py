"""
Handles sending order confirmation emails with PDF invoice attachments.
PDFs include product images, quantities, prices, shipping, and total.
"""

from flask_mail import Message
from app import mail
from jinja2 import Template
import requests
import os

def send_order_confirmation_email(recipient_email, order):
    from weasyprint import HTML
    """
    Sends an order confirmation email with a PDF invoice to the recipient.
    Args:
        recipient_email (str): The recipient's email address.
        order (Order): The order object containing order details.
    """
    msg = Message("Your Order Confirmation", recipients=[recipient_email])
    msg.body = "Thank you for your order! Please find your order details attached."
    pdf_data = generate_order_pdf(order)
    msg.attach("order_confirmation.pdf", "application/pdf", pdf_data)
    mail.send(msg)

def generate_order_pdf(order):
    """
    Generates a PDF invoice for the given order using PDFShift.
    Args:
        order (Order): The order object.
    Returns:
        bytes: The PDF file as bytes.
    """
    # HTML template for the order invoice
    html_template = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            h2 { color: #6c63ff; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background: #f3f3f3; }
            img { max-width: 60px; max-height: 60px; object-fit: cover; }
        </style>
    </head>
    <body>
        <h2>Order Confirmation - Order #{{ order.id }}</h2>
        <p>User ID: {{ order.user_id }}</p>
        <p>Order Date: {{ order.created_at.strftime('%Y-%m-%d') if order.created_at else '' }}</p>
        <p>Status: {{ order.status }}</p>
        <h3>Items:</h3>
        <table>
            <tr>
                <th>Product</th>
                <th>Image</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Subtotal</th>
            </tr>
            {% for item in order.items %}
            <tr>
                <td>{{ item.product.name }}</td>
                <td>
                    {% if item.product.image_gallery %}
                        {% if item.product.image_gallery is string %}
                            <img src="{{ item.product.image_gallery }}">
                        {% else %}
                            <img src="{{ item.product.image_gallery[0] }}">
                        {% endif %}
                    {% endif %}
                </td>
                <td>{{ item.quantity }}</td>
                <td>${{ "%.2f"|format(item.price) }}</td>
                <td>${{ "%.2f"|format(item.price * item.quantity) }}</td>
            </tr>
            {% endfor %}
        </table>
        <div style="margin-top: 20px;">
            <strong>Shipping:</strong> $5.00
        </div>
        <div>
            <strong>Order Total:</strong> ${{ "%.2f"|format(order.total) }}
        </div>
    </body>
    </html>
    """
    # Render HTML with Jinja2
    from jinja2 import Template
    template = Template(html_template)
    html_content = template.render(order=order)

    # Get API key from environment variable
    api_key = os.getenv('PDFSHIFT_API_KEY')
    print("Loaded PDFShift API key:", api_key)
    response = requests.post(
        'https://api.pdfshift.io/v3/convert/pdf',
         headers={ 'X-API-Key': api_key },
        json={'source': html_content}
    )
    if response.status_code == 200:
        return response.content  # PDF bytes
    else:
        raise Exception(f"PDFShift error: {response.text}")