"""
Services pour la logique métier
Architecture MVP
"""

from .base_service import BaseService
from .user_service import UserService
from .product_service import ProductService
from .order_service import OrderService
from .auth_service import AuthService, get_auth_service

__all__ = [
    'BaseService',
    'UserService',
    'ProductService',
    'OrderService',
    'AuthService',
    'get_auth_service'
]