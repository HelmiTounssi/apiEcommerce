"""
Tests unitaires pour les services frontend
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
from services.api_client import ApiClient


class TestAuthService:
    """Tests pour le service d'authentification"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.auth_service = AuthService()
    
    def test_initialization(self):
        """Test d'initialisation du service"""
        assert self.auth_service.token is None
        assert self.auth_service.user is None
    
    @patch('services.auth_service.st.session_state')
    def test_set_token(self, mock_session):
        """Test de définition du token"""
        token = "test_token_123"
        self.auth_service.set_token(token)
        
        assert self.auth_service.token == token
        mock_session.__setitem__.assert_called_with("auth_token", token)
    
    @patch('services.auth_service.st.session_state')
    def test_get_access_token(self, mock_session):
        """Test de récupération du token d'accès"""
        mock_session.get.return_value = "test_token_123"
        
        token = self.auth_service.get_access_token()
        
        assert token == "test_token_123"
        mock_session.get.assert_called_with("access_token", None)
    
    @patch('services.auth_service.st.session_state')
    def test_is_authenticated_true(self, mock_session):
        """Test d'authentification avec token valide"""
        mock_session.get.return_value = "test_token_123"
        
        assert self.auth_service.is_authenticated() is True
    
    @patch('services.auth_service.st.session_state')
    def test_is_authenticated_false(self, mock_session):
        """Test d'authentification sans token"""
        mock_session.get.return_value = None
        
        assert self.auth_service.is_authenticated() is False
    
    @patch('services.auth_service.st.session_state')
    def test_is_admin_true(self, mock_session):
        """Test de vérification admin avec rôle admin"""
        mock_session.get.side_effect = lambda key: {
            "auth_token": "test_token",
            "user_role": "admin"
        }.get(key)
        
        assert self.auth_service.is_admin() is True
    
    @patch('services.auth_service.st.session_state')
    def test_is_admin_false(self, mock_session):
        """Test de vérification admin avec rôle client"""
        mock_session.get.side_effect = lambda key: {
            "auth_token": "test_token",
            "user_role": "client"
        }.get(key)
        
        assert self.auth_service.is_admin() is False


class TestUserService:
    """Tests pour le service utilisateur"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.user_service = UserService()
    
    @patch('services.user_service.ApiClient')
    def test_get_users(self, mock_api_client):
        """Test de récupération des utilisateurs"""
        mock_client = Mock()
        mock_api_client.return_value = mock_client
        mock_client.get.return_value = {
            "success": True,
            "data": [
                {"id": 1, "nom": "User 1", "email": "user1@test.com"},
                {"id": 2, "nom": "User 2", "email": "user2@test.com"}
            ]
        }
        
        users = self.user_service.get_users("test_token")
        
        assert len(users) == 2
        assert users[0]["nom"] == "User 1"
        assert users[1]["nom"] == "User 2"
        mock_client.get.assert_called_with("/utilisateurs", "test_token")
    
    @patch('services.user_service.ApiClient')
    def test_create_user(self, mock_api_client):
        """Test de création d'utilisateur"""
        mock_client = Mock()
        mock_api_client.return_value = mock_client
        mock_client.post.return_value = {
            "success": True,
            "data": {"id": 1, "nom": "New User", "email": "new@test.com"}
        }
        
        user_data = {"nom": "New User", "email": "new@test.com", "password": "password123"}
        result = self.user_service.create_user(user_data, "test_token")
        
        assert result["success"] is True
        assert result["data"]["nom"] == "New User"
        mock_client.post.assert_called_with("/utilisateurs", user_data, "test_token")


class TestProductService:
    """Tests pour le service produit"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.product_service = ProductService()
    
    @patch('services.product_service.ApiClient')
    def test_get_products(self, mock_api_client):
        """Test de récupération des produits"""
        mock_client = Mock()
        mock_api_client.return_value = mock_client
        mock_client.get.return_value = {
            "success": True,
            "data": [
                {"id": 1, "nom": "Product 1", "prix": 99.99},
                {"id": 2, "nom": "Product 2", "prix": 149.99}
            ]
        }
        
        products = self.product_service.get_products("test_token")
        
        assert len(products) == 2
        assert products[0]["nom"] == "Product 1"
        assert products[1]["prix"] == 149.99
        mock_client.get.assert_called_with("/produits", "test_token")
    
    @patch('services.product_service.ApiClient')
    def test_create_product(self, mock_api_client):
        """Test de création de produit"""
        mock_client = Mock()
        mock_api_client.return_value = mock_client
        mock_client.post.return_value = {
            "success": True,
            "data": {"id": 1, "nom": "New Product", "prix": 199.99}
        }
        
        product_data = {"nom": "New Product", "prix": 199.99, "description": "Test"}
        result = self.product_service.create_product(product_data, "test_token")
        
        assert result["success"] is True
        assert result["data"]["nom"] == "New Product"
        mock_client.post.assert_called_with("/produits", product_data, "test_token")


class TestOrderService:
    """Tests pour le service commande"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.order_service = OrderService()
    
    @patch('services.order_service.ApiClient')
    def test_get_orders(self, mock_api_client):
        """Test de récupération des commandes"""
        mock_client = Mock()
        mock_api_client.return_value = mock_client
        mock_client.get.return_value = {
            "success": True,
            "data": [
                {"id": 1, "statut": "en_attente", "total": 199.98},
                {"id": 2, "statut": "confirme", "total": 299.97}
            ]
        }
        
        orders = self.order_service.get_orders("test_token")
        
        assert len(orders) == 2
        assert orders[0]["statut"] == "en_attente"
        assert orders[1]["total"] == 299.97
        mock_client.get.assert_called_with("/commandes", "test_token")
    
    @patch('services.order_service.ApiClient')
    def test_update_order(self, mock_api_client):
        """Test de mise à jour de commande"""
        mock_client = Mock()
        mock_api_client.return_value = mock_client
        mock_client.put.return_value = {
            "success": True,
            "data": {"id": 1, "statut": "confirme", "total": 199.98}
        }
        
        order_id = 1
        update_data = {"statut": "confirme"}
        result = self.order_service.update_order(order_id, update_data, "test_token")
        
        assert result["success"] is True
        assert result["data"]["statut"] == "confirme"
        mock_client.put.assert_called_with(f"/commandes/{order_id}", update_data, "test_token")


class TestApiClient:
    """Tests pour le client API"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.api_client = ApiClient()
    
    @patch('services.api_client.requests.get')
    def test_get_success(self, mock_get):
        """Test de requête GET réussie"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": "test"}
        mock_get.return_value = mock_response
        
        result = self.api_client.get("/test", "token123")
        
        assert result["success"] is True
        assert result["data"] == "test"
        mock_get.assert_called_with(
            "http://localhost:5000/test",
            headers={"Authorization": "Bearer token123"}
        )
    
    @patch('services.api_client.requests.post')
    def test_post_success(self, mock_post):
        """Test de requête POST réussie"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"success": True, "data": "created"}
        mock_post.return_value = mock_response
        
        data = {"name": "test"}
        result = self.api_client.post("/test", data, "token123")
        
        assert result["success"] is True
        assert result["data"] == "created"
        mock_post.assert_called_with(
            "http://localhost:5000/test",
            json=data,
            headers={"Authorization": "Bearer token123"}
        )
    
    @patch('services.api_client.requests.put')
    def test_put_success(self, mock_put):
        """Test de requête PUT réussie"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": "updated"}
        mock_put.return_value = mock_response
        
        data = {"name": "updated"}
        result = self.api_client.put("/test/1", data, "token123")
        
        assert result["success"] is True
        assert result["data"] == "updated"
        mock_put.assert_called_with(
            "http://localhost:5000/test/1",
            json=data,
            headers={"Authorization": "Bearer token123"}
        )
