"""
Tests d'intégration pour le frontend
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Ajouter le chemin du frontend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from services.auth_service import AuthService
from services.user_service import UserService
from services.product_service import ProductService
from services.order_service import OrderService
from models.user import User
from models.product import Product
from models.order import Order


class TestFrontendIntegration:
    """Tests d'intégration pour le frontend"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.auth_service = AuthService()
        self.user_service = UserService()
        self.product_service = ProductService()
        self.order_service = OrderService()
    
    @patch('services.auth_service.st.session_state')
    @patch('services.user_service.ApiClient')
    def test_user_workflow(self, mock_api_client, mock_session):
        """Test du workflow complet utilisateur"""
        # Configuration des mocks
        mock_client = Mock()
        mock_api_client.return_value = mock_client
        
        # Mock de l'authentification
        mock_session.get.side_effect = lambda key: {
            "auth_token": "test_token",
            "user_role": "admin"
        }.get(key)
        
        # Mock de la récupération des utilisateurs
        mock_client.get.return_value = {
            "success": True,
            "data": [
                {"id": 1, "nom": "User 1", "email": "user1@test.com", "role": "client"},
                {"id": 2, "nom": "User 2", "email": "user2@test.com", "role": "admin"},
                {"id": 3, "nom": "User 3", "email": "user3@test.com", "role": "manager"}
            ]
        }
        
        # Test du workflow
        assert self.auth_service.is_authenticated() is True
        assert self.auth_service.is_admin() is True
        
        users = self.user_service.get_users("test_token")
        assert len(users) == 3
        
        # Vérification des données utilisateur
        user1 = users[0]
        assert user1["nom"] == "User 1"
        assert user1["email"] == "user1@test.com"
        assert user1["role"] == "client"
        
        # Vérification du rôle manager
        user3 = users[2]
        assert user3["nom"] == "User 3"
        assert user3["email"] == "user3@test.com"
        assert user3["role"] == "manager"
    
    @patch('services.auth_service.st.session_state')
    @patch('services.product_service.ApiClient')
    def test_product_workflow(self, mock_api_client, mock_session):
        """Test du workflow complet produit"""
        # Configuration des mocks
        mock_client = Mock()
        mock_api_client.return_value = mock_client
        
        # Mock de l'authentification
        mock_session.get.side_effect = lambda key: {
            "auth_token": "test_token",
            "user_role": "admin"
        }.get(key)
        
        # Mock de la récupération des produits
        mock_client.get.return_value = {
            "success": True,
            "data": [
                {"id": 1, "nom": "Product 1", "prix": 99.99, "stock": 10},
                {"id": 2, "nom": "Product 2", "prix": 149.99, "stock": 5}
            ]
        }
        
        # Test du workflow
        assert self.auth_service.is_authenticated() is True
        
        products = self.product_service.get_products("test_token")
        assert len(products) == 2
        
        # Vérification des données produit
        product1 = products[0]
        assert product1["nom"] == "Product 1"
        assert product1["prix"] == 99.99
        assert product1["stock"] == 10
    
    @patch('services.auth_service.st.session_state')
    @patch('services.order_service.ApiClient')
    def test_order_workflow(self, mock_api_client, mock_session):
        """Test du workflow complet commande"""
        # Configuration des mocks
        mock_client = Mock()
        mock_api_client.return_value = mock_client
        
        # Mock de l'authentification
        mock_session.get.side_effect = lambda key: {
            "auth_token": "test_token",
            "user_role": "admin"
        }.get(key)
        
        # Mock de la récupération des commandes
        mock_client.get.return_value = {
            "success": True,
            "data": [
                {"id": 1, "statut": "en_attente", "total": 199.98, "utilisateur_id": 1},
                {"id": 2, "statut": "confirme", "total": 299.97, "utilisateur_id": 2}
            ]
        }
        
        # Mock de la mise à jour de commande
        mock_client.put.return_value = {
            "success": True,
            "data": {"id": 1, "statut": "confirme", "total": 199.98}
        }
        
        # Test du workflow
        assert self.auth_service.is_authenticated() is True
        
        orders = self.order_service.get_orders("test_token")
        assert len(orders) == 2
        
        # Vérification des données commande
        order1 = orders[0]
        assert order1["statut"] == "en_attente"
        assert order1["total"] == 199.98
        
        # Test de mise à jour de commande
        update_result = self.order_service.update_order(1, {"statut": "confirme"}, "test_token")
        assert update_result["success"] is True
        assert update_result["data"]["statut"] == "confirme"
    
    @patch('services.auth_service.st.session_state')
    @patch('services.user_service.ApiClient')
    @patch('services.product_service.ApiClient')
    @patch('services.order_service.ApiClient')
    def test_complete_workflow(self, mock_order_client, mock_product_client, mock_user_client, mock_session):
        """Test du workflow complet de l'application"""
        # Configuration des mocks
        mock_user_client.return_value = Mock()
        mock_product_client.return_value = Mock()
        mock_order_client.return_value = Mock()
        
        # Mock de l'authentification
        mock_session.get.side_effect = lambda key: {
            "auth_token": "test_token",
            "user_role": "admin"
        }.get(key)
        
        # Mock des données
        mock_user_client.return_value.get.return_value = {
            "success": True,
            "data": [{"id": 1, "nom": "Test User", "email": "test@test.com"}]
        }
        
        mock_product_client.return_value.get.return_value = {
            "success": True,
            "data": [{"id": 1, "nom": "Test Product", "prix": 99.99}]
        }
        
        mock_order_client.return_value.get.return_value = {
            "success": True,
            "data": [{"id": 1, "statut": "en_attente", "total": 99.99}]
        }
        
        # Test du workflow complet
        assert self.auth_service.is_authenticated() is True
        assert self.auth_service.is_admin() is True
        
        # Récupération des données
        users = self.user_service.get_users("test_token")
        products = self.product_service.get_products("test_token")
        orders = self.order_service.get_orders("test_token")
        
        # Vérifications
        assert len(users) == 1
        assert len(products) == 1
        assert len(orders) == 1
        
        assert users[0]["nom"] == "Test User"
        assert products[0]["nom"] == "Test Product"
        assert orders[0]["statut"] == "en_attente"
    
    def test_model_integration(self):
        """Test d'intégration des modèles"""
        # Test de création d'utilisateur
        user = User(
            id=1,
            nom="Test User",
            email="test@test.com",
            role="client"
        )
        
        user_dict = user.to_dict()
        assert user_dict["nom"] == "Test User"
        assert user_dict["email"] == "test@test.com"
        
        # Test de création de produit
        product = Product(
            id=1,
            nom="Test Product",
            description="Test Description",
            prix=99.99,
            stock=10,
            categorie="Test Category"
        )
        
        product_dict = product.to_dict()
        assert product_dict["nom"] == "Test Product"
        assert product_dict["prix"] == 99.99
        
        # Test de création de commande
        order = Order(
            id=1,
            utilisateur_id=1,
            statut="en_attente",
            total=99.99,
            date_creation="2023-01-01T00:00:00"
        )
        
        order_dict = order.to_dict()
        assert order_dict["utilisateur_id"] == 1
        assert order_dict["statut"] == "en_attente"
        assert order_dict["total"] == 99.99
    
    def test_user_role_manager_validation(self):
        """Test spécifique de validation du rôle manager"""
        # Test de création d'utilisateur avec rôle manager
        user = User(
            id=1,
            nom="Test Manager",
            email="manager@test.com",
            role="manager"
        )
        
        assert user.role == "manager"
        assert user.nom == "Test Manager"
        assert user.email == "manager@test.com"
        
        # Test de conversion en dictionnaire
        user_dict = user.to_dict()
        assert user_dict["role"] == "manager"
        assert user_dict["nom"] == "Test Manager"
        assert user_dict["email"] == "manager@test.com"
        
        # Test de création à partir d'un dictionnaire
        user_data = {
            "id": 2,
            "nom": "Another Manager",
            "email": "another@test.com",
            "role": "manager",
            "date_creation": "2023-01-01T00:00:00"
        }
        
        user_from_dict = User.from_dict(user_data)
        assert user_from_dict.role == "manager"
        assert user_from_dict.nom == "Another Manager"
        assert user_from_dict.email == "another@test.com"
