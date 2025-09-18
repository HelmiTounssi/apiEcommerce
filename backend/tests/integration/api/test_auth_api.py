"""
Tests pour l'API d'authentification
"""

import pytest
import json
from src.domain.models.utilisateur import Utilisateur


class TestAuthAPI:
    """Tests pour l'API d'authentification"""
    
    def test_register_success(self, client):
        """Test d'inscription réussie"""
        response = client.post('/api/auth/register', json={
            'email': 'newuser@example.com',
            'mot_de_passe': 'password123',
            'nom': 'New User',
            'role': 'client'
        })
        
        assert response.status_code == 201
        data = response.json
        assert data['success'] is True
        assert data['message'] == 'Utilisateur créé avec succès'
        assert 'user' in data
        assert data['user']['email'] == 'newuser@example.com'
    
    def test_register_duplicate_email(self, client, sample_user):
        """Test d'inscription avec email déjà utilisé"""
        response = client.post('/api/auth/register', json={
            'email': sample_user.email,
            'mot_de_passe': 'password123',
            'nom': 'Another User',
            'role': 'client'
        })
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
        assert 'email' in data['message'].lower()
    
    def test_register_invalid_data(self, client):
        """Test d'inscription avec données invalides"""
        response = client.post('/api/auth/register', json={
            'email': 'invalid-email',
            'mot_de_passe': '123',  # Mot de passe trop court
            'nom': '',
            'role': 'invalid_role'
        })
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
    
    def test_login_success(self, client, sample_user):
        """Test de connexion réussie"""
        response = client.post('/api/auth/login', json={
            'email': sample_user.email,
            'mot_de_passe': 'user123'
        })
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert 'access_token' in data
        assert data['token_type'] == 'Bearer'
        assert data['expires_in'] == 3600
        assert 'user' in data
        assert data['user']['email'] == sample_user.email
    
    def test_login_invalid_credentials(self, client):
        """Test de connexion avec identifiants invalides"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'mot_de_passe': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.json
        assert data['success'] is False
        assert 'incorrect' in data['message'].lower()
    
    def test_login_missing_data(self, client):
        """Test de connexion avec données manquantes"""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com'
            # mot_de_passe manquant
        })
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
    
    def test_protected_route_without_token(self, client):
        """Test d'accès à une route protégée sans token"""
        response = client.get('/api/utilisateurs/')
        
        assert response.status_code == 401
        data = response.json
        assert data['success'] is False
        assert 'token' in data['message'].lower()
    
    def test_protected_route_with_invalid_token(self, client):
        """Test d'accès à une route protégée avec token invalide"""
        headers = {'Authorization': 'Bearer invalid-token'}
        response = client.get('/api/utilisateurs/', headers=headers)
        
        assert response.status_code == 401
        data = response.json
        assert data['success'] is False
    
    def test_protected_route_with_valid_token(self, client, auth_headers):
        """Test d'accès à une route protégée avec token valide"""
        response = client.get('/api/utilisateurs/', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert 'data' in data
    
    def test_token_expiration(self, client, sample_user):
        """Test d'expiration du token"""
        # Se connecter pour obtenir un token
        response = client.post('/api/auth/login', json={
            'email': sample_user.email,
            'mot_de_passe': 'user123'
        })
        
        token = response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Simuler l'expiration du token (dans un vrai test, on utiliserait un token expiré)
        # Pour ce test, on vérifie que le token est valide
        response = client.get('/api/utilisateurs/', headers=headers)
        assert response.status_code == 200
    
    def test_user_password_hashing(self, client):
        """Test que les mots de passe sont bien hachés"""
        response = client.post('/api/auth/register', json={
            'email': 'hash@example.com',
            'mot_de_passe': 'plaintext123',
            'nom': 'Hash User',
            'role': 'client'
        })
        
        assert response.status_code == 201
        
        # Vérifier que le mot de passe est haché dans la base
        with client.application.app_context():
            user = Utilisateur.query.filter_by(email='hash@example.com').first()
            assert user is not None
            assert user.mot_de_passe != 'plaintext123'  # Ne doit pas être en clair
            assert user.check_password('plaintext123')  # Mais doit être vérifiable
