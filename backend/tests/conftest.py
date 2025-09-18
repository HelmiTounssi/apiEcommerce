"""
Configuration des tests backend
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Ajouter le chemin du backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.app import create_app
from src.data.database.db import db


@pytest.fixture
def app():
    """Création de l'application Flask pour les tests"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Client de test Flask"""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Session de base de données pour les tests"""
    with app.app_context():
        yield db.session


@pytest.fixture
def admin_user(db_session):
    """Utilisateur administrateur de test"""
    from src.domain.models.utilisateur import Utilisateur
    
    user = Utilisateur(
        nom="Admin Test",
        email="admin@test.com",
        mot_de_passe="admin123",
        role="admin"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def client_user(db_session):
    """Utilisateur client de test"""
    from src.domain.models.utilisateur import Utilisateur
    
    user = Utilisateur(
        nom="Client Test",
        email="client@test.com",
        mot_de_passe="client123",
        role="client"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(admin_user):
    """En-têtes d'authentification pour les tests"""
    from src.service.impl.auth_service import AuthService
    
    auth_service = AuthService()
    token = auth_service.generate_token(admin_user.id, admin_user.role)
    
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_user(db_session):
    """Utilisateur de test générique"""
    import uuid
    from src.domain.models.utilisateur import Utilisateur
    
    user = Utilisateur(
        nom=f"Test User {uuid.uuid4().hex[:8]}",
        email=f"test{uuid.uuid4().hex[:8]}@example.com",
        mot_de_passe="test123",
        role="client"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_product(db_session):
    """Produit de test générique"""
    import uuid
    from src.domain.models.produit import Produit
    
    product = Produit(
        nom=f"Test Product {uuid.uuid4().hex[:8]}",
        description="Test Description",
        prix=99.99,
        stock=10,
        categorie="Test Category"
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture
def sample_order(db_session, sample_user, sample_product):
    """Commande de test générique"""
    from src.domain.models.commande import Commande
    from src.domain.models.ligne_commande import LigneCommande
    
    order = Commande(
        utilisateur_id=sample_user.id,
        statut="en_attente",
        total=99.99
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    
    # Ajouter une ligne de commande
    line_item = LigneCommande(
        commande_id=order.id,
        produit_id=sample_product.id,
        quantite=1,
        prix_unitaire=99.99
    )
    db_session.add(line_item)
    db_session.commit()
    
    return order
