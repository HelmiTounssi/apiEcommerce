"""
Tests pour les modèles de données
"""

import pytest
from datetime import datetime
from src.domain.models.utilisateur import Utilisateur
from src.domain.models.produit import Produit
from src.domain.models.commande import Commande
from src.domain.models.ligne_commande import LigneCommande


class TestUtilisateurModel:
    """Tests pour le modèle Utilisateur"""
    
    def test_utilisateur_creation(self, app):
        """Test de création d'un utilisateur"""
        with app.app_context():
            user = Utilisateur(
                email="test@example.com",
                mot_de_passe="password123",
                nom="Test User",
                role="client"
            )
            
            assert user.email == "test@example.com"
            assert user.nom == "Test User"
            assert user.role == "client"
            assert user.mot_de_passe != "password123"  # Doit être haché
            assert user.date_creation is not None
    
    def test_password_hashing(self, app):
        """Test du hachage des mots de passe"""
        with app.app_context():
            user = Utilisateur(
                email="test@example.com",
                mot_de_passe="password123",
                nom="Test User"
            )
            
            # Le mot de passe doit être haché
            assert user.mot_de_passe != "password123"
            assert len(user.mot_de_passe) > 20  # Hash bcrypt est long
            
            # Mais doit être vérifiable
            assert user.check_password("password123") is True
            assert user.check_password("wrongpassword") is False
    
    def test_utilisateur_to_dict(self, app):
        """Test de conversion en dictionnaire"""
        with app.app_context():
            user = Utilisateur(
                email="test@example.com",
                mot_de_passe="password123",
                nom="Test User",
                role="admin"
            )
            
            user_dict = user.to_dict()
            
            assert user_dict['email'] == "test@example.com"
            assert user_dict['nom'] == "Test User"
            assert user_dict['role'] == "admin"
            assert 'id' in user_dict
            assert 'date_creation' in user_dict
            assert 'mot_de_passe' not in user_dict  # Ne doit pas être exposé
    
    def test_utilisateur_repr(self, app):
        """Test de la représentation string"""
        with app.app_context():
            user = Utilisateur(
                email="test@example.com",
                mot_de_passe="password123",
                nom="Test User"
            )
            
            repr_str = repr(user)
            assert "Utilisateur" in repr_str
            assert "test@example.com" in repr_str


class TestProduitModel:
    """Tests pour le modèle Produit"""
    
    def test_produit_creation(self, app):
        """Test de création d'un produit"""
        with app.app_context():
            product = Produit(
                nom="Test Product",
                description="Test Description",
                categorie="Test Category",
                prix=99.99,
                quantite_stock=50,
                image_url="/static/images/test.jpg",
                images=["/static/images/test.jpg", "/static/images/test2.jpg"]
            )
            
            assert product.nom == "Test Product"
            assert product.description == "Test Description"
            assert product.categorie == "Test Category"
            assert product.prix == 99.99
            assert product.quantite_stock == 50
            assert product.image_url == "/static/images/test.jpg"
            assert product.images == ["/static/images/test.jpg", "/static/images/test2.jpg"]
            # date_creation est défini automatiquement lors de la sauvegarde en base
    
    def test_produit_to_dict(self, app):
        """Test de conversion en dictionnaire"""
        with app.app_context():
            product = Produit(
                nom="Test Product",
                description="Test Description",
                categorie="Test Category",
                prix=99.99,
                quantite_stock=50,
                image_url="/static/images/test.jpg",
                images=["/static/images/test.jpg", "/static/images/test2.jpg"]
            )
            
            product_dict = product.to_dict()
            
            assert product_dict['nom'] == "Test Product"
            assert product_dict['description'] == "Test Description"
            assert product_dict['categorie'] == "Test Category"
            assert product_dict['prix'] == 99.99
            assert product_dict['quantite_stock'] == 50
            assert product_dict['image_url'] == "/static/images/test.jpg"
            assert product_dict['images'] == ["/static/images/test.jpg", "/static/images/test2.jpg"]
            assert 'id' in product_dict
            assert 'date_creation' in product_dict
    
    def test_produit_repr(self, app):
        """Test de la représentation string"""
        with app.app_context():
            product = Produit(
                nom="Test Product",
                description="Test Description",
                categorie="Test Category",
                prix=99.99,
                quantite_stock=50
            )
            
            repr_str = repr(product)
            assert "Produit" in repr_str
            assert "Test Product" in repr_str


class TestCommandeModel:
    """Tests pour le modèle Commande"""
    
    def test_commande_creation(self, app, sample_user):
        """Test de création d'une commande"""
        with app.app_context():
            order = Commande(
                utilisateur_id=sample_user.id,
                adresse_livraison="123 Test Street",
                statut="en_attente"
            )
            
            assert order.utilisateur_id == sample_user.id
            assert order.adresse_livraison == "123 Test Street"
            assert order.statut == "en_attente"
            assert order.date_commande is not None
    
    def test_commande_to_dict(self, app, sample_user):
        """Test de conversion en dictionnaire"""
        with app.app_context():
            order = Commande(
                utilisateur_id=sample_user.id,
                adresse_livraison="123 Test Street",
                statut="validée"
            )
            
            order_dict = order.to_dict()
            
            assert order_dict['utilisateur_id'] == sample_user.id
            assert order_dict['adresse_livraison'] == "123 Test Street"
            assert order_dict['statut'] == "validée"
            assert 'id' in order_dict
            assert 'date_commande' in order_dict
    
    def test_commande_repr(self, app, sample_user):
        """Test de la représentation string"""
        with app.app_context():
            order = Commande(
                utilisateur_id=sample_user.id,
                adresse_livraison="123 Test Street",
                statut="en_attente"
            )
            
            repr_str = repr(order)
            assert "Commande" in repr_str
            assert str(sample_user.id) in repr_str


class TestLigneCommandeModel:
    """Tests pour le modèle LigneCommande"""
    
    def test_ligne_commande_creation(self, app, sample_order, sample_product):
        """Test de création d'une ligne de commande"""
        with app.app_context():
            ligne = LigneCommande(
                commande_id=sample_order.id,
                produit_id=sample_product.id,
                quantite=3,
                prix_unitaire=sample_product.prix
            )
            
            assert ligne.commande_id == sample_order.id
            assert ligne.produit_id == sample_product.id
            assert ligne.quantite == 3
            assert ligne.prix_unitaire == sample_product.prix
    
    def test_ligne_commande_to_dict(self, app, sample_order, sample_product):
        """Test de conversion en dictionnaire"""
        with app.app_context():
            ligne = LigneCommande(
                commande_id=sample_order.id,
                produit_id=sample_product.id,
                quantite=2,
                prix_unitaire=99.99
            )
            
            ligne_dict = ligne.to_dict()
            
            assert ligne_dict['commande_id'] == sample_order.id
            assert ligne_dict['produit_id'] == sample_product.id
            assert ligne_dict['quantite'] == 2
            assert ligne_dict['prix_unitaire'] == 99.99
            assert 'id' in ligne_dict
    
    def test_ligne_commande_repr(self, app, sample_order, sample_product):
        """Test de la représentation string"""
        with app.app_context():
            ligne = LigneCommande(
                commande_id=sample_order.id,
                produit_id=sample_product.id,
                quantite=1,
                prix_unitaire=99.99
            )
            
            repr_str = repr(ligne)
            assert "LigneCommande" in repr_str
            assert str(sample_order.id) in repr_str


class TestModelRelationships:
    """Tests pour les relations entre modèles"""
    
    def test_utilisateur_commande_relationship(self, app, sample_user, sample_order):
        """Test de la relation utilisateur-commande"""
        with app.app_context():
            # Vérifier que la commande est liée à l'utilisateur
            assert sample_order.utilisateur_id == sample_user.id
            assert sample_order.utilisateur == sample_user
            
            # Vérifier que l'utilisateur a accès à ses commandes
            assert sample_order in sample_user.commandes
    
    def test_commande_ligne_commande_relationship(self, app, sample_order, sample_product):
        """Test de la relation commande-ligne de commande"""
        with app.app_context():
            ligne = LigneCommande(
                commande_id=sample_order.id,
                produit_id=sample_product.id,
                quantite=1,
                prix_unitaire=sample_product.prix
            )
            
            # Vérifier que la ligne est liée à la commande
            assert ligne.commande_id == sample_order.id
            assert ligne.commande == sample_order
            
            # Vérifier que la commande a accès à ses lignes
            assert ligne in sample_order.lignes_commande
    
    def test_cascade_deletion(self, app, sample_user, sample_order, sample_product):
        """Test de suppression en cascade"""
        with app.app_context():
            # Créer une ligne de commande
            ligne = LigneCommande(
                commande_id=sample_order.id,
                produit_id=sample_product.id,
                quantite=1,
                prix_unitaire=sample_product.prix
            )
            
            # Supprimer l'utilisateur
            db.session.delete(sample_user)
            db.session.commit()
            
            # Vérifier que la commande et la ligne sont supprimées
            assert Commande.query.get(sample_order.id) is None
            assert LigneCommande.query.get(ligne.id) is None
