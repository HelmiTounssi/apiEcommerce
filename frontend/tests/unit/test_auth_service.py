"""
Tests unitaires pour le service d'authentification frontend
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Ajouter le chemin du frontend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from services.auth_service import AuthService


class TestAuthService:
    """Tests pour le service d'authentification"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.auth_service = AuthService()
    
    @patch('services.auth_service.st.session_state')
    def test_get_access_token_exists(self, mock_session):
        """Test de récupération du token d'accès quand il existe"""
        # Configuration du mock
        mock_session.get.return_value = "test_token_123"
        
        # Test
        token = self.auth_service.get_access_token()
        
        # Vérifications
        assert token == "test_token_123"
        mock_session.get.assert_called_once_with('access_token', None)
    
    @patch('services.auth_service.st.session_state')
    def test_get_access_token_not_exists(self, mock_session):
        """Test de récupération du token d'accès quand il n'existe pas"""
        # Configuration du mock
        mock_session.get.return_value = None
        
        # Test
        token = self.auth_service.get_access_token()
        
        # Vérifications
        assert token is None
        mock_session.get.assert_called_once_with('access_token', None)
    
    @patch('services.auth_service.st.session_state')
    def test_is_authenticated_true(self, mock_session):
        """Test de vérification d'authentification quand l'utilisateur est connecté"""
        # Configuration du mock
        mock_session.get.return_value = True
        
        # Test
        is_auth = self.auth_service.is_authenticated()
        
        # Vérifications
        assert is_auth is True
        mock_session.get.assert_called_once_with('is_authenticated', False)
    
    @patch('services.auth_service.st.session_state')
    def test_is_authenticated_false(self, mock_session):
        """Test de vérification d'authentification quand l'utilisateur n'est pas connecté"""
        # Configuration du mock
        mock_session.get.return_value = False
        
        # Test
        is_auth = self.auth_service.is_authenticated()
        
        # Vérifications
        assert is_auth is False
        mock_session.get.assert_called_once_with('is_authenticated', False)
    
    @patch('services.auth_service.st.session_state')
    def test_get_current_user_exists(self, mock_session):
        """Test de récupération de l'utilisateur actuel quand il existe"""
        # Configuration du mock
        user_data = {
            "id": 1,
            "nom": "Test User",
            "email": "test@example.com",
            "role": "admin"
        }
        mock_session.get.return_value = user_data
        
        # Test
        user = self.auth_service.get_current_user()
        
        # Vérifications
        assert user == user_data
        mock_session.get.assert_called_once_with('user', None)
    
    @patch('services.auth_service.st.session_state')
    def test_get_current_user_not_exists(self, mock_session):
        """Test de récupération de l'utilisateur actuel quand il n'existe pas"""
        # Configuration du mock
        mock_session.get.return_value = None
        
        # Test
        user = self.auth_service.get_current_user()
        
        # Vérifications
        assert user is None
        mock_session.get.assert_called_once_with('user', None)
    
    @patch('services.auth_service.st.session_state')
    def test_is_admin_true(self, mock_session):
        """Test de vérification du rôle admin quand l'utilisateur est admin"""
        # Configuration du mock
        user_data = {
            "id": 1,
            "nom": "Admin User",
            "email": "admin@example.com",
            "role": "admin"
        }
        mock_session.get.return_value = user_data
        
        # Test
        is_admin = self.auth_service.is_admin()
        
        # Vérifications
        assert is_admin is True
        mock_session.get.assert_called_once_with('user', None)
    
    @patch('services.auth_service.st.session_state')
    def test_is_admin_false(self, mock_session):
        """Test de vérification du rôle admin quand l'utilisateur n'est pas admin"""
        # Configuration du mock
        user_data = {
            "id": 1,
            "nom": "Client User",
            "email": "client@example.com",
            "role": "client"
        }
        mock_session.get.return_value = user_data
        
        # Test
        is_admin = self.auth_service.is_admin()
        
        # Vérifications
        assert is_admin is False
        mock_session.get.assert_called_once_with('user', None)
    
    @patch('services.auth_service.st.session_state')
    def test_is_admin_no_user(self, mock_session):
        """Test de vérification du rôle admin quand aucun utilisateur n'est connecté"""
        # Configuration du mock
        mock_session.get.return_value = None
        
        # Test
        is_admin = self.auth_service.is_admin()
        
        # Vérifications
        assert is_admin is False
        mock_session.get.assert_called_once_with('user', None)
    
    @patch('services.auth_service.st.session_state')
    def test_is_client_true(self, mock_session):
        """Test de vérification du rôle client quand l'utilisateur est client"""
        # Configuration du mock
        user_data = {
            "id": 1,
            "nom": "Client User",
            "email": "client@example.com",
            "role": "client"
        }
        mock_session.get.return_value = user_data
        
        # Test
        is_client = self.auth_service.is_client()
        
        # Vérifications
        assert is_client is True
        mock_session.get.assert_called_once_with('user', None)
    
    @patch('services.auth_service.st.session_state')
    def test_is_client_false(self, mock_session):
        """Test de vérification du rôle client quand l'utilisateur n'est pas client"""
        # Configuration du mock
        user_data = {
            "id": 1,
            "nom": "Admin User",
            "email": "admin@example.com",
            "role": "admin"
        }
        mock_session.get.return_value = user_data
        
        # Test
        is_client = self.auth_service.is_client()
        
        # Vérifications
        assert is_client is False
        mock_session.get.assert_called_once_with('user', None)
    
    def test_auth_service_initialization(self):
        """Test d'initialisation du service d'authentification"""
        # Test
        auth_service = AuthService()
        
        # Vérifications
        assert auth_service.base_url == "http://localhost:5000"
        assert auth_service.api_client is not None
    
    @patch('services.auth_service.st.session_state')
    def test_logout(self, mock_session):
        """Test de déconnexion"""
        # Configuration du mock
        mock_session.__contains__ = Mock(side_effect=lambda key: key in ['access_token', 'user', 'is_authenticated'])
        
        # Test
        self.auth_service.logout()
        
        # Vérifications
        # Vérifier que les clés de session sont supprimées
        assert mock_session.__delitem__.call_count >= 3  # Au moins 3 clés supprimées
    
    @patch('services.auth_service.st.session_state')
    def test_verify_token_valid(self, mock_session):
        """Test de vérification de token valide"""
        # Configuration du mock
        mock_session.get.return_value = "valid_token"
        
        # Test
        is_valid = self.auth_service.verify_token()
        
        # Vérifications
        assert is_valid is True
        mock_session.get.assert_called_once_with('access_token', None)
    
    @patch('services.auth_service.st.session_state')
    def test_verify_token_invalid(self, mock_session):
        """Test de vérification de token invalide"""
        # Configuration du mock
        mock_session.get.return_value = None
        
        # Test
        is_valid = self.auth_service.verify_token()
        
        # Vérifications
        assert is_valid is False
        mock_session.get.assert_called_once_with('access_token', None)
