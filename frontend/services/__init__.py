"""
Services pour la logique métier
Architecture MVP
"""

from services.base_service import BaseService
from services.user_service import UserService
from services.product_service import ProductService
from services.order_service import OrderService
from services.auth_service import AuthService, get_auth_service
from services.cart_service import CartService, get_cart_service

__all__ = [
    'BaseService',
    'UserService',
    'ProductService',
    'OrderService',
    'AuthService',
    'get_auth_service',
    'CartService',
    'get_cart_service'
]