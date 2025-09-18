"""
Tests pour l'API des commandes
"""

import pytest
import json


class TestOrderAPI:
    """Tests pour l'API des commandes"""
    
    def test_get_orders_unauthorized(self, client):
        """Test d'accès à la liste des commandes sans authentification"""
        response = client.get('/api/commandes/')
        assert response.status_code == 401
    
    def test_get_orders_success(self, client, auth_headers):
        """Test de récupération de la liste des commandes"""
        response = client.get('/api/commandes/', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert 'data' in data
        assert isinstance(data['data'], list)
    
    def test_get_order_by_id_success(self, client, auth_headers, sample_order):
        """Test de récupération d'une commande par ID"""
        response = client.get(f'/api/commandes/{sample_order.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert data['data']['id'] == sample_order.id
        assert data['data']['utilisateur_id'] == sample_order.utilisateur_id
    
    def test_get_order_by_id_not_found(self, client, auth_headers):
        """Test de récupération d'une commande inexistante"""
        response = client.get('/api/commandes/999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
        assert 'not found' in data['message'].lower()
    
    def test_create_order_success(self, client, auth_headers, sample_user, sample_product):
        """Test de création d'une commande"""
        order_data = {
            'utilisateur_id': sample_user.id,
            'adresse_livraison': '123 New Street, City',
            'statut': 'en_attente',
            'lignes_commande': [
                {
                    'produit_id': sample_product.id,
                    'quantite': 2,
                    'prix_unitaire': sample_product.prix
                }
            ]
        }
        
        response = client.post('/api/commandes/', json=order_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json
        assert data['success'] is True
        assert data['data']['utilisateur_id'] == order_data['utilisateur_id']
        assert data['data']['adresse_livraison'] == order_data['adresse_livraison']
        assert data['data']['statut'] == order_data['statut']
    
    def test_create_order_invalid_data(self, client, auth_headers):
        """Test de création d'une commande avec données invalides"""
        order_data = {
            'utilisateur_id': 999,  # Utilisateur inexistant
            'adresse_livraison': '',  # Adresse vide
            'statut': 'invalid_status',
            'lignes_commande': []
        }
        
        response = client.post('/api/commandes/', json=order_data, headers=auth_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
    
    def test_update_order_success(self, client, auth_headers, sample_order):
        """Test de mise à jour d'une commande"""
        update_data = {
            'adresse_livraison': '456 Updated Street, City',
            'statut': 'validée'
        }
        
        response = client.put(f'/api/commandes/{sample_order.id}', json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert data['data']['adresse_livraison'] == update_data['adresse_livraison']
        assert data['data']['statut'] == update_data['statut']
    
    def test_update_order_not_found(self, client, auth_headers):
        """Test de mise à jour d'une commande inexistante"""
        update_data = {
            'statut': 'validée'
        }
        
        response = client.put('/api/commandes/999', json=update_data, headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
    
    def test_delete_order_success(self, client, auth_headers, sample_order):
        """Test de suppression d'une commande"""
        response = client.delete(f'/api/commandes/{sample_order.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert 'deleted' in data['message'].lower()
    
    def test_delete_order_not_found(self, client, auth_headers):
        """Test de suppression d'une commande inexistante"""
        response = client.delete('/api/commandes/999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.json
        assert data['success'] is False
    
    def test_order_status_validation(self, client, auth_headers, sample_order):
        """Test de validation du statut de commande"""
        # Test statut invalide
        response = client.put(f'/api/commandes/{sample_order.id}', json={
            'statut': 'invalid_status'
        }, headers=auth_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
        
        # Test statuts valides
        valid_statuses = ['en_attente', 'validée', 'expédiée', 'annulée']
        for status in valid_statuses:
            response = client.put(f'/api/commandes/{sample_order.id}', json={
                'statut': status
            }, headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['statut'] == status
    
    def test_order_line_items(self, client, auth_headers, sample_user, sample_product):
        """Test de gestion des lignes de commande"""
        order_data = {
            'utilisateur_id': sample_user.id,
            'adresse_livraison': '123 Test Street',
            'statut': 'en_attente',
            'lignes_commande': [
                {
                    'produit_id': sample_product.id,
                    'quantite': 3,
                    'prix_unitaire': sample_product.prix
                }
            ]
        }
        
        response = client.post('/api/commandes/', json=order_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json
        assert data['success'] is True
        assert len(data['data']['lignes_commande']) == 1
        assert data['data']['lignes_commande'][0]['quantite'] == 3
    
    def test_order_filtering_by_user(self, client, auth_headers, sample_user, sample_product):
        """Test de filtrage des commandes par utilisateur"""
        # Créer des commandes pour différents utilisateurs
        for i in range(3):
            order_data = {
                'utilisateur_id': sample_user.id,
                'adresse_livraison': f'{i} Test Street',
                'statut': 'en_attente',
                'lignes_commande': [
                    {
                        'produit_id': sample_product.id,
                        'quantite': 1,
                        'prix_unitaire': sample_product.prix
                    }
                ]
            }
            client.post('/api/commandes/', json=order_data, headers=auth_headers)
        
        # Test filtrage par utilisateur
        response = client.get(f'/api/commandes/?utilisateur_id={sample_user.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert len(data['data']) >= 3
    
    def test_order_filtering_by_status(self, client, auth_headers, sample_user, sample_product):
        """Test de filtrage des commandes par statut"""
        # Créer des commandes avec différents statuts
        statuses = ['en_attente', 'validée', 'expédiée']
        for status in statuses:
            order_data = {
                'utilisateur_id': sample_user.id,
                'adresse_livraison': f'Test Street {status}',
                'statut': status,
                'lignes_commande': [
                    {
                        'produit_id': sample_product.id,
                        'quantite': 1,
                        'prix_unitaire': sample_product.prix
                    }
                ]
            }
            client.post('/api/commandes/', json=order_data, headers=auth_headers)
        
        # Test filtrage par statut
        response = client.get('/api/commandes/?statut=en_attente', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert len(data['data']) >= 1
    
    def test_order_pagination(self, client, auth_headers, sample_user, sample_product):
        """Test de pagination des commandes"""
        # Créer plusieurs commandes
        for i in range(5):
            order_data = {
                'utilisateur_id': sample_user.id,
                'adresse_livraison': f'{i} Test Street',
                'statut': 'en_attente',
                'lignes_commande': [
                    {
                        'produit_id': sample_product.id,
                        'quantite': 1,
                        'prix_unitaire': sample_product.prix
                    }
                ]
            }
            client.post('/api/commandes/', json=order_data, headers=auth_headers)
        
        # Test avec pagination
        response = client.get('/api/commandes/?page=1&per_page=3', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['success'] is True
        assert len(data['data']) <= 3
    
    def test_order_total_calculation(self, client, auth_headers, sample_user, sample_product):
        """Test de calcul du total de commande"""
        order_data = {
            'utilisateur_id': sample_user.id,
            'adresse_livraison': '123 Test Street',
            'statut': 'en_attente',
            'lignes_commande': [
                {
                    'produit_id': sample_product.id,
                    'quantite': 2,
                    'prix_unitaire': sample_product.prix
                }
            ]
        }
        
        response = client.post('/api/commandes/', json=order_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json
        assert data['success'] is True
        
        # Vérifier que le total est calculé correctement
        expected_total = sample_product.prix * 2
        assert data['data']['total'] == expected_total

    def test_order_update_request_model(self):
        """Test du modèle UpdateOrderRequest"""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'frontend'))
        
        from frontend.models.order import UpdateOrderRequest
        
        # Test création avec statut seulement
        request1 = UpdateOrderRequest(statut="validée")
        assert request1.statut == "validée"
        assert request1.adresse_livraison is None
        
        # Test création avec adresse seulement
        request2 = UpdateOrderRequest(adresse_livraison="123 New Street")
        assert request2.adresse_livraison == "123 New Street"
        assert request2.statut is None
        
        # Test création avec les deux
        request3 = UpdateOrderRequest(
            adresse_livraison="456 Complete Street",
            statut="expédiée"
        )
        assert request3.adresse_livraison == "456 Complete Street"
        assert request3.statut == "expédiée"
        
        # Test conversion en dictionnaire
        dict1 = request1.to_dict()
        assert dict1 == {"statut": "validée"}
        
        dict2 = request2.to_dict()
        assert dict2 == {"adresse_livraison": "123 New Street"}
        
        dict3 = request3.to_dict()
        assert dict3 == {
            "adresse_livraison": "456 Complete Street",
            "statut": "expédiée"
        }
        
        # Test que utilisateur_id n'est pas accepté
        import pytest
        with pytest.raises(TypeError, match="unexpected keyword argument 'utilisateur_id'"):
            UpdateOrderRequest(utilisateur_id=1, statut="validée")
