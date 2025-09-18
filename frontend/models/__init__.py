"""
Modèles de données pour le frontend
Architecture MVP
"""

from .user import User, CreateUserRequest, UpdateUserRequest
from .product import Product, CreateProductRequest, UpdateProductRequest, UpdateStockRequest
from .order import Order, OrderLine, CreateOrderRequest, UpdateOrderRequest, UpdateOrderStatusRequest
from .cart import Cart, CartItem, CartSummary, AddToCartRequest, UpdateCartQuantityRequest, RemoveFromCartRequest

__all__ = [
    # User models
    'User', 'CreateUserRequest', 'UpdateUserRequest',
    # Product models
    'Product', 'CreateProductRequest', 'UpdateProductRequest', 'UpdateStockRequest',
    # Order models
    'Order', 'OrderLine', 'CreateOrderRequest', 'UpdateOrderRequest', 'UpdateOrderStatusRequest',
    # Cart models
    'Cart', 'CartItem', 'CartSummary', 'AddToCartRequest', 'UpdateCartQuantityRequest', 'RemoveFromCartRequest'
]