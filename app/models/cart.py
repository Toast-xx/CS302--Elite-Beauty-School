# Models for shopping cart and cart items.
# Cart is linked to a user and contains multiple CartItems.
# CartItem links to a product and tracks quantity.
# Cascade delete ensures cart items are removed when a cart is deleted.
# The product relationship in CartItem allows easy access to product details.

from app import db


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    items = db.relationship('CartItem', backref='carts', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "items": self.items
        }


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    # Relationship to Product for convenient access to product details
    product = db.relationship('Product')


    def to_dict(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }

