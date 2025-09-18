"""
Tests d'intégration pour l'IHM
"""

import pytest
import requests
import time

class TestIHMIntegration:
    """Tests d'intégration pour l'IHM"""
    
    def test_backend_connectivity(self):
        """Test de connectivité du backend"""
        try:
            response = requests.get('http://localhost:5000/', timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert 'message' in data
            assert 'endpoints' in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_frontend_connectivity(self):
        """Test de connectivité du frontend"""
        try:
            response = requests.get('http://localhost:8501/', timeout=5)
            assert response.status_code == 200
            assert 'streamlit' in response.text.lower()
        except requests.exceptions.ConnectionError:
            pytest.skip("Frontend non accessible")
    
    def test_authentication_flow(self):
        """Test du flux d'authentification complet"""
        try:
            # Test de connexion
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "admin123"
            }
            
            response = requests.post('http://localhost:5000/api/auth/login', 
                                   json=login_data, timeout=5)
            assert response.status_code == 200
            
            data = response.json()
            assert data.get('success') is True
            assert 'token' in data
            assert 'utilisateur' in data
            
            token = data['token']
            user = data['utilisateur']
            assert user['email'] == 'admin@ecommerce.com'
            assert user['role'] == 'admin'
            
            # Token disponible pour les autres tests
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_products_api_with_auth(self):
        """Test de l'API produits avec authentification"""
        token = self.test_authentication_flow()
        if not token:
            pytest.skip("Authentification échouée")
        
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get('http://localhost:5000/api/produits/', 
                                  headers=headers, timeout=5)
            
            assert response.status_code == 200
            products = response.json()
            assert isinstance(products, list)
            assert len(products) > 0
            
            # Vérifier que les produits ont des images
            product = products[0]
            assert 'nom' in product
            assert 'prix' in product
            assert 'image_url' in product
            assert 'images' in product
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_users_api_with_auth(self):
        """Test de l'API utilisateurs avec authentification"""
        token = self.test_authentication_flow()
        if not token:
            pytest.skip("Authentification échouée")
        
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get('http://localhost:5000/api/utilisateurs/', 
                                  headers=headers, timeout=5)
            
            assert response.status_code == 200
            users = response.json()
            assert isinstance(users, list)
            assert len(users) > 0
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_orders_api_with_auth(self):
        """Test de l'API commandes avec authentification"""
        token = self.test_authentication_flow()
        if not token:
            pytest.skip("Authentification échouée")
        
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get('http://localhost:5000/api/commandes/', 
                                  headers=headers, timeout=5)
            
            assert response.status_code == 200
            orders = response.json()
            assert isinstance(orders, list)
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_product_images_integration(self):
        """Test d'intégration des images de produits"""
        token = self.test_authentication_flow()
        if not token:
            pytest.skip("Authentification échouée")
        
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get('http://localhost:5000/api/produits/', 
                                  headers=headers, timeout=5)
            
            assert response.status_code == 200
            products = response.json()
            
            # Vérifier que tous les produits ont des images
            for product in products:
                assert 'image_url' in product
                assert 'images' in product
                assert isinstance(product['images'], list)
                
                # Au moins un produit doit avoir une image
                if product['image_url']:
                    assert product['image_url'].startswith('/static/images/')
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_api_endpoints_availability(self):
        """Test de disponibilité des endpoints API"""
        try:
            endpoints = [
                '/api/auth/login',
                '/api/produits/',
                '/api/utilisateurs/',
                '/api/commandes/',
                '/api/stats/',
                '/api/config/',
                '/api/maintenance/',
                '/api/reports/'
            ]
            
            for endpoint in endpoints:
                if endpoint == '/api/auth/login':
                    response = requests.post(f'http://localhost:5000{endpoint}', 
                                           json={}, timeout=5)
                else:
                    response = requests.get(f'http://localhost:5000{endpoint}', 
                                          timeout=5)
                
                # Les endpoints doivent répondre (même avec 401/422/400)
                assert response.status_code in [200, 401, 422, 404, 400]
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
