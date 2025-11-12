"""
    - Imports all model classes for use throughout the application.
    - Allows convenient access to models via 'from app.models import ...'.
    - Ensures all models are registered with SQLAlchemy and available for migrations and queries.
    - Includes: Campus, User, Product, Cart, Category, SubCategory, Order, OrderItem, CampusProduct.
"""

from .campus import *
from .user import *
from .product import *
from .cart import *
from .category import Category, SubCategory
from .order import Order, OrderItem
from .campus_products import CampusProduct