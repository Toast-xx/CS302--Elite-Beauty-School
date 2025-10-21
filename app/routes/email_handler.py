from flask_mail import Message
from app import mail
from weasyprint import HTML
from jinja2 import Template

def send_order_confirmation_email(recipient_email, order):
    msg = Message("Your Order Confirmation", recipients=[recipient_email])
    msg.body = "Thank you for your order! Please find your order details attached."
    pdf_data = generate_order_pdf(order)
    msg.attach("order_confirmation.pdf", "application/pdf", pdf_data)
    mail.send(msg)

def generate_order_pdf(order):
    # Create HTML for the order invoice
    html_template = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            h2 { color: #6c63ff; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background: #f3f3f3; }
        </style>
    </head>
    <body>
        <h2>Order Confirmation - Order #{{ order.id }}</h2>
        <p>User ID: {{ order.user_id }}</p>
        <p>Order Date: {{ order.created_at.strftime('%Y-%m-%d') if order.created_at else '' }}</p>
        <p>Status: {{ order.status }}</p>
        <p>Total: ${{ "%.2f"|format(order.total) }}</p>
        <h3>Items:</h3>
        <table>
            <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Subtotal</th>
            </tr>
            {% for item in order.items %}
            <tr>
                <td>{{ item.product.name }}</td>
                <td>{{ item.quantity }}</td>
                <td>${{ "%.2f"|format(item.price) }}</td>
                <td>${{ "%.2f"|format(item.price * item.quantity) }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    # Render HTML with Jinja2
    template = Template(html_template)
    html_content = template.render(order=order)
    # Generate PDF from HTML
    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes