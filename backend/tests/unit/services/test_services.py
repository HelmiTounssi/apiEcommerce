"""
Tests pour les services métier
"""

import pytest
from unittest.mock import Mock, patch
from src.service.impl.auth_service import AuthService
from src.service.impl.utilisateur_service import UtilisateurService
from src.service.impl.produit_service import ProduitService
from src.service.impl.commande_service import CommandeService
from src.domain.models.utilisateur import Utilisateur
from src.domain.models.produit import Produit
from src.domain.models.commande import Commande


class TestAuthService:
    """Tests pour le service d'authentification"""
    
    def test_authenticate_user_success(self, app, sample_user):
        """Test d'authentification réussie"""
        with app.app_context():
            auth_service = AuthService()
            
            result = auth_service.authenticate_user(sample_user.email, "user123")
            
            assert result is not None
            assert result['success'] is True
            assert 'access_token' in result
            assert result['user']['email'] == sample_user.email
    
    def test_authenticate_user_invalid_email(self, app):
        """Test d'authentification avec email invalide"""
        with app.app_context():
            auth_service = AuthService()
            
            result = auth_service.authenticate_user("nonexistent@example.com", "password")
            
            assert result is not None
            assert result['success'] is False
            assert 'incorrect' in result['message'].lower()
    
    def test_authenticate_user_invalid_password(self, app, sample_user):
        """Test d'authentification avec mot de passe invalide"""
        with app.app_context():
            auth_service = AuthService()
            
            result = auth_service.authenticate_user(sample_user.email, "wrongpassword")
            
            assert result is not None
            assert result['success'] is False
            assert 'incorrect' in result['message'].lower()
    
    def test_generate_token(self, app, sample_user):
        """Test de génération de token JWT"""
        with app.app_context():
            auth_service = AuthService()
            
            token = auth_service.generate_token(sample_user)
            
            assert token is not None
            assert isinstance(token, str)
            assert len(token) > 50  # JWT tokens sont longs
    
    def test_verify_token_valid(self, app, sample_user):
        """Test de vérification de token valide"""
        with app.app_context():
            auth_service = AuthService()
            
            # Générer un token
            token = auth_service.generate_token(sample_user)
            
            # Vérifier le token
            result = auth_service.verify_token(token)
            
            assert result is not None
            assert result['success'] is True
            assert result['user']['email'] == sample_user.email
    
    def test_verify_token_invalid(self, app):
        """Test de vérification de token invalide"""
        with app.app_context():
            auth_service = AuthService()
            
            result = auth_service.verify_token("invalid-token")
            
            assert result is not None
            assert result['success'] is False


class TestUtilisateurService:
    """Tests pour le service utilisateur"""
    
    def test_create_user_success(self, app):
        """Test de création d'utilisateur réussie"""
        with app.app_context():
            user_service = UtilisateurService()
            
            user_data = {
                'email': 'newuser@test.com',
                'mot_de_passe': 'password123',
                'nom': 'New User',
                'role': 'client'
            }
            
            result = user_service.create_user(user_data)
            
            assert result is not None
            assert result['success'] is True
            assert result['data']['email'] == user_data['email']
            assert result['data']['nom'] == user_data['nom']
    
    def test_create_user_duplicate_email(self, app, sample_user):
        """Test de création d'utilisateur avec email dupliqué"""
        with app.app_context():
            user_service = UtilisateurService()
            
            user_data = {
                'email': sample_user.email,
                'mot_de_passe': 'password123',
                'nom': 'Another User',
                'role': 'client'
            }
            
            result = user_service.create_user(user_data)
            
            assert result is not None
            assert result['success'] is False
            assert 'email' in result['message'].lower()
    
    def test_get_user_by_id_success(self, app, sample_user):
        """Test de récupération d'utilisateur par ID"""
        with app.app_context():
            user_service = UtilisateurService()
            
            result = user_service.get_user_by_id(sample_user.id)
            
            assert result is not None
            assert result['success'] is True
            assert result['data']['id'] == sample_user.id
            assert result['data']['email'] == sample_user.email
    
    def test_get_user_by_id_not_found(self, app):
        """Test de récupération d'utilisateur inexistant"""
        with app.app_context():
            user_service = UtilisateurService()
            
            result = user_service.get_user_by_id(999)
            
            assert result is not None
            assert result['success'] is False
            assert 'not found' in result['message'].lower()
    
    def test_update_user_success(self, app, sample_user):
        """Test de mise à jour d'utilisateur"""
        with app.app_context():
            user_service = UtilisateurService()
            
            update_data = {
                'nom': 'Updated Name',
                'role': 'admin'
            }
            
            result = user_service.update_user(sample_user.id, update_data)
            
            assert result is not None
            assert result['success'] is True
            assert result['data']['nom'] == update_data['nom']
            assert result['data']['role'] == update_data['role']
    
    def test_delete_user_success(self, app, sample_user):
        """Test de suppression d'utilisateur"""
        with app.app_context():
            user_service = UtilisateurService()
            
            result = user_service.delete_user(sample_user.id)
            
            assert result is not None
            assert result['success'] is True
            assert 'deleted' in result['message'].lower()


class TestProduitService:
    """Tests pour le service produit"""
    
    def test_create_product_success(self, app):
        """Test de création de produit réussie"""
        with app.app_context():
            product_service = ProduitService()
            
            product_data = {
                'nom': 'New Product',
                'description': 'A new test product',
                'categorie': 'Test Category',
                'prix': 199.99,
                'quantite_stock': 50
            }
            
            result = product_service.create_product(product_data)
            
            assert result is not None
            assert result['success'] is True
            assert result['data']['nom'] == product_data['nom']
            assert result['data']['prix'] == product_data['prix']
    
    def test_get_product_by_id_success(self, app, sample_product):
        """Test de récupération de produit par ID"""
        with app.app_context():
            product_service = ProduitService()
            
            result = product_service.get_product_by_id(sample_product.id)
            
            assert result is not None
            assert result['success'] is True
            assert result['data']['id'] == sample_product.id
            assert result['data']['nom'] == sample_product.nom
    
    def test_update_product_success(self, app, sample_product):
        """Test de mise à jour de produit"""
        with app.app_context():
            product_service = ProduitService()
            
            update_data = {
                'prix': 299.99,
                'quantite_stock': 25
            }
            
            result = product_service.update_product(sample_product.id, update_data)
            
            assert result is not None
            assert result['success'] is True
            assert result['data']['prix'] == update_data['prix']
            assert result['data']['quantite_stock'] == update_data['quantite_stock']
    
    def test_search_products(self, app):
        """Test de recherche de produits"""
        with app.app_context():
            product_service = ProduitService()
            
            # Créer des produits de test
            products = [
                {'nom': 'iPhone 15', 'categorie': 'Smartphone', 'prix': 999.99},
                {'nom': 'Samsung Galaxy', 'categorie': 'Smartphone', 'prix': 899.99},
                {'nom': 'MacBook Pro', 'categorie': 'Laptop', 'prix': 1999.99}
            ]
            
            for product_data in products:
                product_service.create_product({
                    **product_data,
                    'description': 'Test description',
                    'quantite_stock': 10
                })
            
            # Test recherche par nom
            result = product_service.search_products(search="iPhone")
            assert result['success'] is True
            assert len(result['data']) >= 1
            
            # Test recherche par catégorie
            result = product_service.search_products(categorie="Smartphone")
            assert result['success'] is True
            assert len(result['data']) >= 2


class TestCommandeService:
    """Tests pour le service commande"""
    
    def test_create_order_success(self, app, sample_user, sample_product):
        """Test de création de commande réussie"""
        with app.app_context():
            order_service = CommandeService()
            
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
            
            result = order_service.create_order(order_data)
            
            assert result is not None
            assert result['success'] is True
            assert result['data']['utilisateur_id'] == order_data['utilisateur_id']
            assert result['data']['statut'] == order_data['statut']
            assert len(result['data']['lignes_commande']) == 1
    
    def test_get_order_by_id_success(self, app, sample_order):
        """Test de récupération de commande par ID"""
        with app.app_context():
            order_service = CommandeService()
            
            result = order_service.get_order_by_id(sample_order.id)
            
            assert result is not None
            assert result['success'] is True
            assert result['data']['id'] == sample_order.id
            assert result['data']['utilisateur_id'] == sample_order.utilisateur_id
    
    def test_update_order_success(self, app, sample_order):
        """Test de mise à jour de commande"""
        with app.app_context():
            order_service = CommandeService()
            
            update_data = {
                'statut': 'validée',
                'adresse_livraison': '456 Updated Street'
            }
            
            result = order_service.update_order(sample_order.id, update_data)
            
            assert result is not None
            assert result['success'] is True
            assert result['data']['statut'] == update_data['statut']
            assert result['data']['adresse_livraison'] == update_data['adresse_livraison']
    
    def test_calculate_order_total(self, app, sample_user, sample_product):
        """Test de calcul du total de commande"""
        with app.app_context():
            order_service = CommandeService()
            
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
            
            result = order_service.create_order(order_data)
            
            assert result is not None
            assert result['success'] is True
            
            # Vérifier le calcul du total
            expected_total = sample_product.prix * 3
            assert result['data']['total'] == expected_total
    
    def test_get_orders_by_user(self, app, sample_user, sample_product):
        """Test de récupération des commandes par utilisateur"""
        with app.app_context():
            order_service = CommandeService()
            
            # Créer plusieurs commandes pour le même utilisateur
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
                order_service.create_order(order_data)
            
            # Récupérer les commandes de l'utilisateur
            result = order_service.get_orders_by_user(sample_user.id)
            
            assert result is not None
            assert result['success'] is True
            assert len(result['data']) >= 3
            
            # Vérifier que toutes les commandes appartiennent à l'utilisateur
            for order in result['data']:
                assert order['utilisateur_id'] == sample_user.id
