"""
Présentateurs pour la logique de présentation
Architecture MVP
"""

from .base_presenter import BasePresenter
from .user_presenter import UserPresenter
from .product_presenter import ProductPresenter
from .order_presenter import OrderPresenter

__all__ = [
    'BasePresenter',
    'UserPresenter',
    'ProductPresenter',
    'OrderPresenter'
]