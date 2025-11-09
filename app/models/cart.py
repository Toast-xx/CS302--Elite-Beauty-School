"""
Models for shopping cart and cart items.
Cart is linked to a user and contains multiple CartItems.
CartItem links to a campus product and tracks quantity.
Cascade delete ensures cart items are removed when a cart is deleted.
"""

from app import db

class Cart(db.Model):
    """
    Represents a user's shopping cart.
    """
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    items = db.relationship('CartItem', backref='carts', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        """
        Convert the Cart object to a dictionary.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "items": self.items
        }

class CartItem(db.Model):
    """
    Represents an item in a user's cart, linked to a campus product.
    """
    __tablename__ = "cart_item"
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    campus_product_id = db.Column(db.Integer, db.ForeignKey('campus_products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    campus_product = db.relationship('CampusProduct')

    def to_dict(self):
        """
        Convert the CartItem object to a dictionary.
        """
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }