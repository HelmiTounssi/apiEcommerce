"""
Tests pour l'API des utilisateurs
"""

import pytest
import json


class TestUserAPI:
    """Tests pour l'API des utilisateurs"""
    
    def test_get_users_unauthorized(self, client):
        """Test d'accès à la liste des utilisateurs sans authentification"""
        response = client.get('/api/utilisateurs/')
        assert response.status_code == 401
    
    def test_get_users_success(self, client, auth_headers):
        """Test de récupération de la liste des utilisateurs"""
        response = client.get('/api/utilisateurs/', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert 'data' in data
        assert isinstance(data['data'], list)
    
    def test_get_user_by_id_success(self, client, auth_headers, sample_user):
        """Test de récupération d'un utilisateur par ID"""
        response = client.get(f'/api/utilisateurs/{sample_user.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert data['data']['id'] == sample_user.id
        assert data['data']['email'] == sample_user.email
    
    def test_get_user_by_id_not_found(self, client, auth_headers):
        """Test de récupération d'un utilisateur inexistant"""
        response = client.get('/api/utilisateurs/999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
        assert 'not found' in data['message'].lower()
    
    def test_create_user_success(self, client, auth_headers):
        """Test de création d'un utilisateur"""
        user_data = {
            'email': 'newuser@test.com',
            'mot_de_passe': 'password123',
            'nom': 'New User',
            'role': 'client'
        }
        
        response = client.post('/api/utilisateurs/', json=user_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json
        assert data['success'] is True
        assert data['data']['email'] == user_data['email']
        assert data['data']['nom'] == user_data['nom']
        assert data['data']['role'] == user_data['role']
    
    def test_create_user_duplicate_email(self, client, auth_headers, sample_user):
        """Test de création d'un utilisateur avec email déjà utilisé"""
        user_data = {
            'email': sample_user.email,
            'mot_de_passe': 'password123',
            'nom': 'Another User',
            'role': 'client'
        }
        
        response = client.post('/api/utilisateurs/', json=user_data, headers=auth_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
        assert 'email' in data['message'].lower()
    
    def test_create_user_invalid_data(self, client, auth_headers):
        """Test de création d'un utilisateur avec données invalides"""
        user_data = {
            'email': 'invalid-email',
            'mot_de_passe': '123',  # Trop court
            'nom': '',
            'role': 'invalid_role'
        }
        
        response = client.post('/api/utilisateurs/', json=user_data, headers=auth_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
    
    def test_update_user_success(self, client, auth_headers, sample_user):
        """Test de mise à jour d'un utilisateur"""
        update_data = {
            'nom': 'Updated Name',
            'role': 'admin'
        }
        
        response = client.put(f'/api/utilisateurs/{sample_user.id}', json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert data['data']['nom'] == update_data['nom']
        assert data['data']['role'] == update_data['role']
    
    def test_update_user_not_found(self, client, auth_headers):
        """Test de mise à jour d'un utilisateur inexistant"""
        update_data = {
            'nom': 'Updated Name'
        }
        
        response = client.put('/api/utilisateurs/999', json=update_data, headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
    
    def test_delete_user_success(self, client, auth_headers, sample_user):
        """Test de suppression d'un utilisateur"""
        response = client.delete(f'/api/utilisateurs/{sample_user.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert 'deleted' in data['message'].lower()
    
    def test_delete_user_not_found(self, client, auth_headers):
        """Test de suppression d'un utilisateur inexistant"""
        response = client.delete('/api/utilisateurs/999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
    
    def test_user_validation(self, client, auth_headers):
        """Test de validation des données utilisateur"""
        # Test email invalide
        response = client.post('/api/utilisateurs/', json={
            'email': 'not-an-email',
            'mot_de_passe': 'password123',
            'nom': 'Test User',
            'role': 'client'
        }, headers=auth_headers)
        
        assert response.status_code == 400
        
        # Test mot de passe trop court
        response = client.post('/api/utilisateurs/', json={
            'email': 'test@example.com',
            'mot_de_passe': '123',
            'nom': 'Test User',
            'role': 'client'
        }, headers=auth_headers)
        
        assert response.status_code == 400
        
        # Test nom vide
        response = client.post('/api/utilisateurs/', json={
            'email': 'test@example.com',
            'mot_de_passe': 'password123',
            'nom': '',
            'role': 'client'
        }, headers=auth_headers)
        
        assert response.status_code == 400
    
    def test_user_role_validation(self, client, auth_headers):
        """Test de validation du rôle utilisateur"""
        response = client.post('/api/utilisateurs/', json={
            'email': 'test@example.com',
            'mot_de_passe': 'password123',
            'nom': 'Test User',
            'role': 'invalid_role'
        }, headers=auth_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
    
    def test_user_pagination(self, client, auth_headers):
        """Test de pagination des utilisateurs"""
        # Créer plusieurs utilisateurs
        for i in range(5):
            client.post('/api/utilisateurs/', json={
                'email': f'user{i}@test.com',
                'mot_de_passe': 'password123',
                'nom': f'User {i}',
                'role': 'client'
            }, headers=auth_headers)
        
        # Test avec pagination
        response = client.get('/api/utilisateurs/?page=1&per_page=3', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert len(data['data']) <= 3
