"""
Tests d'intégration pour l'API complète
"""

import pytest
import json


class TestIntegration:
    """Tests d'intégration pour l'API complète"""
    
    def test_complete_user_workflow(self, client):
        """Test du workflow complet d'un utilisateur"""
        # 1. Inscription
        register_response = client.post('/api/auth/register', json={
            'email': 'integration@test.com',
            'mot_de_passe': 'password123',
            'nom': 'Integration User',
            'role': 'client'
        })
        
        assert register_response.status_code == 201
        user_data = register_response.json['user']
        user_id = user_data['id']
        
        # 2. Connexion
        login_response = client.post('/api/auth/login', json={
            'email': 'integration@test.com',
            'mot_de_passe': 'password123'
        })
        
        assert login_response.status_code == 200
        token = login_response.json['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 3. Récupération du profil
        profile_response = client.get(f'/api/utilisateurs/{user_id}', headers=headers)
        assert profile_response.status_code == 200
        assert profile_response.json['data']['email'] == 'integration@test.com'
        
        # 4. Mise à jour du profil
        update_response = client.put(f'/api/utilisateurs/{user_id}', json={
            'nom': 'Updated Integration User'
        }, headers=headers)
        
        assert update_response.status_code == 200
        assert update_response.json['data']['nom'] == 'Updated Integration User'
    
    def test_complete_product_workflow(self, client, auth_headers):
        """Test du workflow complet d'un produit"""
        # 1. Création d'un produit
        product_response = client.post('/api/produits/', json={
            'nom': 'Integration Product',
            'description': 'A product for integration testing',
            'categorie': 'Test Category',
            'prix': 199.99,
            'quantite_stock': 100
        }, headers=auth_headers)
        
        assert product_response.status_code == 201
        product_data = product_response.json['data']
        product_id = product_data['id']
        
        # 2. Récupération du produit
        get_response = client.get(f'/api/produits/{product_id}', headers=auth_headers)
        assert get_response.status_code == 200
        assert get_response.json['data']['nom'] == 'Integration Product'
        
        # 3. Mise à jour du produit
        update_response = client.put(f'/api/produits/{product_id}', json={
            'prix': 299.99,
            'quantite_stock': 50
        }, headers=auth_headers)
        
        assert update_response.status_code == 200
        assert update_response.json['data']['prix'] == 299.99
        assert update_response.json['data']['quantite_stock'] == 50
        
        # 4. Suppression du produit
        delete_response = client.delete(f'/api/produits/{product_id}', headers=auth_headers)
        assert delete_response.status_code == 200
        
        # 5. Vérification de la suppression
        get_deleted_response = client.get(f'/api/produits/{product_id}', headers=auth_headers)
        assert get_deleted_response.status_code == 404
    
    def test_complete_order_workflow(self, client, auth_headers, sample_user, sample_product):
        """Test du workflow complet d'une commande"""
        # 1. Création d'une commande
        order_response = client.post('/api/commandes/', json={
            'utilisateur_id': sample_user.id,
            'adresse_livraison': '123 Integration Street',
            'statut': 'en_attente',
            'lignes_commande': [
                {
                    'produit_id': sample_product.id,
                    'quantite': 2,
                    'prix_unitaire': sample_product.prix
                }
            ]
        }, headers=auth_headers)
        
        assert order_response.status_code == 201
        order_data = order_response.json['data']
        order_id = order_data['id']
        
        # 2. Récupération de la commande
        get_response = client.get(f'/api/commandes/{order_id}', headers=auth_headers)
        assert get_response.status_code == 200
        assert get_response.json['data']['statut'] == 'en_attente'
        
        # 3. Mise à jour du statut
        update_response = client.put(f'/api/commandes/{order_id}', json={
            'statut': 'validée'
        }, headers=auth_headers)
        
        assert update_response.status_code == 200
        assert update_response.json['data']['statut'] == 'validée'
        
        # 4. Mise à jour de l'adresse
        address_update_response = client.put(f'/api/commandes/{order_id}', json={
            'adresse_livraison': '456 Updated Integration Street'
        }, headers=auth_headers)
        
        assert address_update_response.status_code == 200
        assert address_update_response.json['data']['adresse_livraison'] == '456 Updated Integration Street'
        
        # 5. Finalisation de la commande
        finalize_response = client.put(f'/api/commandes/{order_id}', json={
            'statut': 'expédiée'
        }, headers=auth_headers)
        
        assert finalize_response.status_code == 200
        assert finalize_response.json['data']['statut'] == 'expédiée'
    
    def test_admin_vs_client_permissions(self, client, sample_user, sample_product):
        """Test des permissions admin vs client"""
        # Créer un utilisateur client
        client_user_response = client.post('/api/auth/register', json={
            'email': 'client@integration.com',
            'mot_de_passe': 'password123',
            'nom': 'Client User',
            'role': 'client'
        })
        
        client_user_id = client_user_response.json['user']['id']
        
        # Connexion client
        client_login = client.post('/api/auth/login', json={
            'email': 'client@integration.com',
            'mot_de_passe': 'password123'
        })
        
        client_token = client_login.json['access_token']
        client_headers = {'Authorization': f'Bearer {client_token}'}
        
        # Créer un utilisateur admin
        admin_user_response = client.post('/api/auth/register', json={
            'email': 'admin@integration.com',
            'mot_de_passe': 'password123',
            'nom': 'Admin User',
            'role': 'admin'
        })
        
        # Connexion admin
        admin_login = client.post('/api/auth/login', json={
            'email': 'admin@integration.com',
            'mot_de_passe': 'password123'
        })
        
        admin_token = admin_login.json['access_token']
        admin_headers = {'Authorization': f'Bearer {admin_token}'}
        
        # Test: Client peut voir ses propres données
        client_profile = client.get(f'/api/utilisateurs/{client_user_id}', headers=client_headers)
        assert client_profile.status_code == 200
        
        # Test: Client peut créer des commandes
        client_order = client.post('/api/commandes/', json={
            'utilisateur_id': client_user_id,
            'adresse_livraison': '123 Client Street',
            'statut': 'en_attente',
            'lignes_commande': [
                {
                    'produit_id': sample_product.id,
                    'quantite': 1,
                    'prix_unitaire': sample_product.prix
                }
            ]
        }, headers=client_headers)
        
        assert client_order.status_code == 201
        
        # Test: Admin peut voir tous les utilisateurs
        all_users = client.get('/api/utilisateurs/', headers=admin_headers)
        assert all_users.status_code == 200
        assert len(all_users.json['data']) >= 2  # Au moins client et admin
        
        # Test: Admin peut gérer les produits
        admin_product = client.post('/api/produits/', json={
            'nom': 'Admin Product',
            'description': 'Product created by admin',
            'categorie': 'Admin Category',
            'prix': 99.99,
            'quantite_stock': 50
        }, headers=admin_headers)
        
        assert admin_product.status_code == 201
    
    def test_data_consistency(self, client, auth_headers, sample_user, sample_product):
        """Test de cohérence des données"""
        # Créer une commande
        order_response = client.post('/api/commandes/', json={
            'utilisateur_id': sample_user.id,
            'adresse_livraison': '123 Consistency Street',
            'statut': 'en_attente',
            'lignes_commande': [
                {
                    'produit_id': sample_product.id,
                    'quantite': 3,
                    'prix_unitaire': sample_product.prix
                }
            ]
        }, headers=auth_headers)
        
        order_id = order_response.json['data']['id']
        
        # Vérifier la cohérence des données
        order_data = client.get(f'/api/commandes/{order_id}', headers=auth_headers).json['data']
        user_data = client.get(f'/api/utilisateurs/{sample_user.id}', headers=auth_headers).json['data']
        product_data = client.get(f'/api/produits/{sample_product.id}', headers=auth_headers).json['data']
        
        # Vérifier les relations
        assert order_data['utilisateur_id'] == sample_user.id
        assert order_data['utilisateur_id'] == user_data['id']
        assert len(order_data['lignes_commande']) == 1
        assert order_data['lignes_commande'][0]['produit_id'] == sample_product.id
        assert order_data['lignes_commande'][0]['produit_id'] == product_data['id']
        
        # Vérifier le calcul du total
        expected_total = sample_product.prix * 3
        assert order_data['total'] == expected_total
    
    def test_error_handling_consistency(self, client, auth_headers):
        """Test de cohérence de la gestion d'erreurs"""
        # Test d'erreurs 404
        not_found_endpoints = [
            '/api/utilisateurs/999',
            '/api/produits/999',
            '/api/commandes/999'
        ]
        
        for endpoint in not_found_endpoints:
            response = client.get(endpoint, headers=auth_headers)
            assert response.status_code == 404
            data = response.json
            assert data['success'] is False
            assert 'not found' in data['message'].lower()
        
        # Test d'erreurs 400
        invalid_data_tests = [
            ('/api/utilisateurs/', {'email': 'invalid-email'}),
            ('/api/produits/', {'nom': '', 'prix': -10}),
            ('/api/commandes/', {'utilisateur_id': 999, 'adresse_livraison': ''})
        ]
        
        for endpoint, invalid_data in invalid_data_tests:
            response = client.post(endpoint, json=invalid_data, headers=auth_headers)
            assert response.status_code == 400
            data = response.json
            assert data['success'] is False
    
    def test_api_response_format_consistency(self, client, auth_headers):
        """Test de cohérence du format des réponses API"""
        # Test format de réponse pour les listes
        list_endpoints = ['/api/utilisateurs/', '/api/produits/', '/api/commandes/']
        
        for endpoint in list_endpoints:
            response = client.get(endpoint, headers=auth_headers)
            assert response.status_code == 200
            data = response.json
            
            # Vérifier la structure de base
            assert 'success' in data
            assert 'data' in data
            assert isinstance(data['data'], list)
            assert data['success'] is True
        
        # Test format de réponse pour les éléments individuels
        # (nécessite des données existantes)
        users_response = client.get('/api/utilisateurs/', headers=auth_headers)
        if users_response.json['data']:
            user_id = users_response.json['data'][0]['id']
            user_response = client.get(f'/api/utilisateurs/{user_id}', headers=auth_headers)
            
            data = user_response.json
            assert 'success' in data
            assert 'data' in data
            assert isinstance(data['data'], dict)
            assert data['success'] is True
