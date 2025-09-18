"""
Tests unitaires pour les modèles frontend
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Ajouter le chemin du frontend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from models.user import User
from models.product import Product
from models.order import Order, UpdateOrderRequest


class TestUserModel:
    """Tests pour le modèle User"""
    
    def test_user_creation(self):
        """Test de création d'un utilisateur"""
        user = User(
            id=1,
            nom="Test User",
            email="test@example.com",
            role="client"
        )
        
        assert user.id == 1
        assert user.nom == "Test User"
        assert user.email == "test@example.com"
        assert user.role == "client"
    
    def test_user_to_dict(self):
        """Test de conversion en dictionnaire"""
        user = User(
            id=1,
            nom="Test User",
            email="test@example.com",
            role="client"
        )
        
        user_dict = user.to_dict()
        
        assert user_dict["id"] == 1
        assert user_dict["nom"] == "Test User"
        assert user_dict["email"] == "test@example.com"
        assert user_dict["role"] == "client"
    
    def test_user_role_validation_client(self):
        """Test de validation du rôle client"""
        user = User(
            id=1,
            nom="Test User",
            email="test@example.com",
            role="client"
        )
        assert user.role == "client"
    
    def test_user_role_validation_admin(self):
        """Test de validation du rôle admin"""
        user = User(
            id=1,
            nom="Test Admin",
            email="admin@example.com",
            role="admin"
        )
        assert user.role == "admin"
    
    def test_user_role_validation_manager(self):
        """Test de validation du rôle manager"""
        user = User(
            id=1,
            nom="Test Manager",
            email="manager@example.com",
            role="manager"
        )
        assert user.role == "manager"
    
    def test_user_role_validation_invalid(self):
        """Test de validation d'un rôle invalide"""
        with pytest.raises(ValueError, match="Le rôle doit être 'client', 'admin' ou 'manager'"):
            User(
                id=1,
                nom="Test User",
                email="test@example.com",
                role="invalid_role"
            )
    
    def test_user_from_dict_with_manager_role(self):
        """Test de création d'utilisateur à partir d'un dictionnaire avec rôle manager"""
        user_data = {
            "id": 1,
            "nom": "Test Manager",
            "email": "manager@example.com",
            "role": "manager",
            "date_creation": "2023-01-01T00:00:00"
        }
        
        user = User.from_dict(user_data)
        
        assert user.id == 1
        assert user.nom == "Test Manager"
        assert user.email == "manager@example.com"
        assert user.role == "manager"


class TestProductModel:
    """Tests pour le modèle Product"""
    
    def test_product_creation(self):
        """Test de création d'un produit"""
        product = Product(
            id=1,
            nom="Test Product",
            description="Test Description",
            prix=99.99,
            quantite_stock=10,
            categorie="Test Category",
            image_url="/static/images/test.jpg",
            images=["/static/images/test.jpg", "/static/images/test2.jpg"]
        )
        
        assert product.id == 1
        assert product.nom == "Test Product"
        assert product.description == "Test Description"
        assert product.prix == 99.99
        assert product.quantite_stock == 10
        assert product.categorie == "Test Category"
        assert product.image_url == "/static/images/test.jpg"
        assert product.images == ["/static/images/test.jpg", "/static/images/test2.jpg"]
    
    def test_product_to_dict(self):
        """Test de conversion en dictionnaire"""
        product = Product(
            id=1,
            nom="Test Product",
            description="Test Description",
            prix=99.99,
            quantite_stock=10,
            categorie="Test Category",
            image_url="/static/images/test.jpg",
            images=["/static/images/test.jpg", "/static/images/test2.jpg"]
        )
        
        product_dict = product.to_dict()
        
        assert product_dict["id"] == 1
        assert product_dict["nom"] == "Test Product"
        assert product_dict["prix"] == 99.99


class TestOrderModel:
    """Tests pour le modèle Order"""
    
    def test_order_creation(self):
        """Test de création d'une commande"""
        order = Order(
            id=1,
            utilisateur_id=1,
            statut="en_attente",
            total=199.98,
            date_creation="2023-01-01T00:00:00"
        )
        
        assert order.id == 1
        assert order.utilisateur_id == 1
        assert order.statut == "en_attente"
        assert order.total == 199.98
        assert order.date_creation == "2023-01-01T00:00:00"
    
    def test_order_to_dict(self):
        """Test de conversion en dictionnaire"""
        order = Order(
            id=1,
            utilisateur_id=1,
            statut="en_attente",
            total=199.98,
            date_creation="2023-01-01T00:00:00"
        )
        
        order_dict = order.to_dict()
        
        assert order_dict["id"] == 1
        assert order_dict["utilisateur_id"] == 1
        assert order_dict["statut"] == "en_attente"
        assert order_dict["total"] == 199.98


class TestUpdateOrderRequest:
    """Tests pour le modèle UpdateOrderRequest"""
    
    def test_update_order_request_creation(self):
        """Test de création d'une requête de mise à jour"""
        request = UpdateOrderRequest(
            statut="confirme",
            total=299.99
        )
        
        assert request.statut == "confirme"
        assert request.total == 299.99
    
    def test_update_order_request_to_dict(self):
        """Test de conversion en dictionnaire"""
        request = UpdateOrderRequest(
            statut="confirme",
            total=299.99
        )
        
        request_dict = request.to_dict()
        
        assert request_dict["statut"] == "confirme"
        assert request_dict["total"] == 299.99
    
    def test_update_order_request_partial(self):
        """Test de mise à jour partielle"""
        request = UpdateOrderRequest(statut="confirme")
        
        assert request.statut == "confirme"
        assert request.total is None
