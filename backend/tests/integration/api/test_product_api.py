"""
Tests pour l'API des produits
"""

import pytest
import json


class TestProductAPI:
    """Tests pour l'API des produits"""
    
    def test_get_products_unauthorized(self, client):
        """Test d'accès à la liste des produits sans authentification"""
        response = client.get('/api/produits/')
        assert response.status_code == 401
    
    def test_get_products_success(self, client, auth_headers):
        """Test de récupération de la liste des produits"""
        response = client.get('/api/produits/', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert 'data' in data
        assert isinstance(data['data'], list)
    
    def test_get_product_by_id_success(self, client, auth_headers, sample_product):
        """Test de récupération d'un produit par ID"""
        response = client.get(f'/api/produits/{sample_product.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert data['data']['id'] == sample_product.id
        assert data['data']['nom'] == sample_product.nom
    
    def test_get_product_by_id_not_found(self, client, auth_headers):
        """Test de récupération d'un produit inexistant"""
        response = client.get('/api/produits/999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
        assert 'not found' in data['message'].lower()
    
    def test_create_product_success(self, client, auth_headers):
        """Test de création d'un produit"""
        product_data = {
            'nom': 'New Product',
            'description': 'A new test product',
            'categorie': 'Test Category',
            'prix': 199.99,
            'quantite_stock': 50,
            'image_url': '/static/images/new-product.jpg',
            'images': ['/static/images/new-product.jpg', '/static/images/new-product-2.jpg']
        }
        
        response = client.post('/api/produits/', json=product_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json
        assert data['success'] is True
        assert data['data']['nom'] == product_data['nom']
        assert data['data']['prix'] == product_data['prix']
        assert data['data']['quantite_stock'] == product_data['quantite_stock']
        assert data['data']['image_url'] == product_data['image_url']
        assert data['data']['images'] == product_data['images']
    
    def test_create_product_invalid_data(self, client, auth_headers):
        """Test de création d'un produit avec données invalides"""
        product_data = {
            'nom': '',  # Nom vide
            'description': 'A test product',
            'categorie': 'Test Category',
            'prix': -10,  # Prix négatif
            'quantite_stock': -5  # Stock négatif
        }
        
        response = client.post('/api/produits/', json=product_data, headers=auth_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
    
    def test_update_product_success(self, client, auth_headers, sample_product):
        """Test de mise à jour d'un produit"""
        update_data = {
            'nom': 'Updated Product Name',
            'prix': 299.99,
            'quantite_stock': 25
        }
        
        response = client.put(f'/api/produits/{sample_product.id}', json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert data['data']['nom'] == update_data['nom']
        assert data['data']['prix'] == update_data['prix']
        assert data['data']['quantite_stock'] == update_data['quantite_stock']
    
    def test_update_product_not_found(self, client, auth_headers):
        """Test de mise à jour d'un produit inexistant"""
        update_data = {
            'nom': 'Updated Product'
        }
        
        response = client.put('/api/produits/999', json=update_data, headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
    
    def test_delete_product_success(self, client, auth_headers, sample_product):
        """Test de suppression d'un produit"""
        response = client.delete(f'/api/produits/{sample_product.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert 'deleted' in data['message'].lower()
    
    def test_delete_product_not_found(self, client, auth_headers):
        """Test de suppression d'un produit inexistant"""
        response = client.delete('/api/produits/999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
    
    def test_product_validation(self, client, auth_headers):
        """Test de validation des données produit"""
        # Test nom vide
        response = client.post('/api/produits/', json={
            'nom': '',
            'description': 'Test description',
            'categorie': 'Test Category',
            'prix': 99.99,
            'quantite_stock': 10
        }, headers=auth_headers)
        
        assert response.status_code == 400
        
        # Test prix négatif
        response = client.post('/api/produits/', json={
            'nom': 'Test Product',
            'description': 'Test description',
            'categorie': 'Test Category',
            'prix': -99.99,
            'quantite_stock': 10
        }, headers=auth_headers)
        
        assert response.status_code == 400
        
        # Test stock négatif
        response = client.post('/api/produits/', json={
            'nom': 'Test Product',
            'description': 'Test description',
            'categorie': 'Test Category',
            'prix': 99.99,
            'quantite_stock': -10
        }, headers=auth_headers)
        
        assert response.status_code == 400
    
    def test_product_search(self, client, auth_headers):
        """Test de recherche de produits"""
        # Créer des produits de test
        products = [
            {'nom': 'iPhone 15', 'categorie': 'Smartphone', 'prix': 999.99},
            {'nom': 'Samsung Galaxy', 'categorie': 'Smartphone', 'prix': 899.99},
            {'nom': 'MacBook Pro', 'categorie': 'Laptop', 'prix': 1999.99}
        ]
        
        for product in products:
            client.post('/api/produits/', json={
                **product,
                'description': 'Test description',
                'quantite_stock': 10
            }, headers=auth_headers)
        
        # Test recherche par nom
        response = client.get('/api/produits/?search=iPhone', headers=auth_headers)
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert len(data['data']) >= 1
        
        # Test recherche par catégorie
        response = client.get('/api/produits/?categorie=Smartphone', headers=auth_headers)
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert len(data['data']) >= 2
    
    def test_product_filtering(self, client, auth_headers):
        """Test de filtrage des produits"""
        # Créer des produits avec différents prix
        products = [
            {'nom': 'Cheap Product', 'prix': 10.99, 'categorie': 'Budget'},
            {'nom': 'Expensive Product', 'prix': 1000.99, 'categorie': 'Premium'}
        ]
        
        for product in products:
            client.post('/api/produits/', json={
                **product,
                'description': 'Test description',
                'quantite_stock': 10
            }, headers=auth_headers)
        
        # Test filtrage par prix minimum
        response = client.get('/api/produits/?min_price=100', headers=auth_headers)
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        
        # Test filtrage par prix maximum
        response = client.get('/api/produits/?max_price=50', headers=auth_headers)
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
    
    def test_product_pagination(self, client, auth_headers):
        """Test de pagination des produits"""
        # Créer plusieurs produits
        for i in range(5):
            client.post('/api/produits/', json={
                'nom': f'Product {i}',
                'description': f'Description {i}',
                'categorie': 'Test Category',
                'prix': 99.99 + i,
                'quantite_stock': 10
            }, headers=auth_headers)
        
        # Test avec pagination
        response = client.get('/api/produits/?page=1&per_page=3', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert len(data['data']) <= 3
