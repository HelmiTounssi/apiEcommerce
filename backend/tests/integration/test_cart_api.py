"""
Tests d'intégration pour l'API du panier
"""

import pytest
import requests
import json


class TestCartAPI:
    """Tests pour l'API du panier"""
    
    def test_get_cart_unauthorized(self):
        """Test d'accès au panier sans authentification"""
        try:
            response = requests.get('http://localhost:5000/api/panier/', timeout=5)
            # Devrait retourner 200 avec un panier de session vide
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_get_cart_with_auth(self):
        """Test d'accès au panier avec authentification"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # Test du panier
            response = requests.get('http://localhost:5000/api/panier/', 
                                  headers=headers, timeout=5)
            assert response.status_code == 200
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_add_to_cart_with_auth(self):
        """Test d'ajout au panier avec authentification"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # Ajouter un produit au panier
            cart_data = {
                "produit_id": 1,
                "quantite": 2
            }
            
            response = requests.post('http://localhost:5000/api/panier/ajouter',
                                   json=cart_data, headers=headers, timeout=5)
            
            assert response.status_code == 200
            data = response.json()
            assert data.get('success') is True
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_add_to_cart_without_auth(self):
        """Test d'ajout au panier sans authentification (session)"""
        try:
            headers = {'X-Session-ID': 'test-session-123'}
            
            # Ajouter un produit au panier
            cart_data = {
                "produit_id": 1,
                "quantite": 1
            }
            
            response = requests.post('http://localhost:5000/api/panier/ajouter',
                                   json=cart_data, headers=headers, timeout=5)
            
            assert response.status_code == 200
            data = response.json()
            assert data.get('success') is True
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_update_cart_quantity(self):
        """Test de modification de quantité dans le panier"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # D'abord ajouter un produit
            cart_data = {
                "produit_id": 1,
                "quantite": 1
            }
            
            add_response = requests.post('http://localhost:5000/api/panier/ajouter',
                                       json=cart_data, headers=headers, timeout=5)
            assert add_response.status_code == 200
            
            # Puis modifier la quantité
            update_data = {
                "produit_id": 1,
                "quantite": 3
            }
            
            response = requests.put('http://localhost:5000/api/panier/modifier-quantite',
                                  json=update_data, headers=headers, timeout=5)
            
            assert response.status_code == 200
            data = response.json()
            assert data.get('success') is True
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_remove_from_cart(self):
        """Test de suppression d'un produit du panier"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # D'abord ajouter un produit
            cart_data = {
                "produit_id": 1,
                "quantite": 1
            }
            
            add_response = requests.post('http://localhost:5000/api/panier/ajouter',
                                       json=cart_data, headers=headers, timeout=5)
            assert add_response.status_code == 200
            
            # Puis supprimer le produit
            remove_data = {
                "produit_id": 1
            }
            
            response = requests.delete('http://localhost:5000/api/panier/supprimer',
                                     json=remove_data, headers=headers, timeout=5)
            
            assert response.status_code == 200
            data = response.json()
            assert data.get('success') is True
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_clear_cart(self):
        """Test de vidage du panier"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # D'abord ajouter des produits
            cart_data = {
                "produit_id": 1,
                "quantite": 2
            }
            
            add_response = requests.post('http://localhost:5000/api/panier/ajouter',
                                       json=cart_data, headers=headers, timeout=5)
            assert add_response.status_code == 200
            
            # Puis vider le panier
            response = requests.delete('http://localhost:5000/api/panier/vider',
                                     headers=headers, timeout=5)
            
            assert response.status_code == 200
            data = response.json()
            assert data.get('success') is True
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_get_cart_summary(self):
        """Test de récupération du résumé du panier"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # Récupérer le résumé
            response = requests.get('http://localhost:5000/api/panier/resume',
                                  headers=headers, timeout=5)
            
            assert response.status_code == 200
            data = response.json()
            assert 'nombre_items' in data
            assert 'total' in data
            assert 'items' in data
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_cart_migration(self):
        """Test de migration du panier de session vers utilisateur"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            headers['X-Session-ID'] = 'test-session-migration'
            
            # Ajouter un produit en session
            cart_data = {
                "produit_id": 1,
                "quantite": 1
            }
            
            add_response = requests.post('http://localhost:5000/api/panier/ajouter',
                                       json=cart_data, headers=headers, timeout=5)
            assert add_response.status_code == 200
            
            # Migrer le panier
            response = requests.post('http://localhost:5000/api/panier/migrer',
                                   headers=headers, timeout=5)
            
            assert response.status_code == 200
            data = response.json()
            assert data.get('success') is True
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_cart_invalid_product(self):
        """Test d'ajout d'un produit inexistant au panier"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # Ajouter un produit inexistant
            cart_data = {
                "produit_id": 99999,
                "quantite": 1
            }
            
            response = requests.post('http://localhost:5000/api/panier/ajouter',
                                   json=cart_data, headers=headers, timeout=5)
            
            assert response.status_code == 400
            data = response.json()
            assert data.get('success') is False
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_cart_insufficient_stock(self):
        """Test d'ajout avec stock insuffisant"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # Ajouter une quantité excessive
            cart_data = {
                "produit_id": 1,
                "quantite": 99999
            }
            
            response = requests.post('http://localhost:5000/api/panier/ajouter',
                                   json=cart_data, headers=headers, timeout=5)
            
            assert response.status_code == 400
            data = response.json()
            assert data.get('success') is False
            assert 'stock' in data.get('message', '').lower()
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
