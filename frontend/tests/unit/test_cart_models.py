"""
Tests unitaires pour les modèles de panier
"""

import pytest
from datetime import datetime
from models.cart import Cart, CartItem, CartSummary, AddToCartRequest, UpdateCartQuantityRequest, RemoveFromCartRequest


class TestCartItem:
    """Tests pour le modèle CartItem"""
    
    def test_cart_item_creation(self):
        """Test de création d'un item de panier"""
        item = CartItem(
            id=1,
            panier_id=1,
            produit_id=1,
            quantite=2,
            prix_unitaire=10.50,
            sous_total=21.00
        )
        
        assert item.id == 1
        assert item.panier_id == 1
        assert item.produit_id == 1
        assert item.quantite == 2
        assert item.prix_unitaire == 10.50
        assert item.sous_total == 21.00
    
    def test_cart_item_validation(self):
        """Test de validation d'un item de panier"""
        # Test avec des valeurs valides
        item = CartItem(
            produit_id=1,
            quantite=1,
            prix_unitaire=10.0
        )
        assert item.produit_id == 1
        
        # Test avec produit_id invalide
        with pytest.raises(ValueError, match="L'ID du produit est requis"):
            CartItem(produit_id=0, quantite=1, prix_unitaire=10.0)
        
        # Test avec quantité invalide
        with pytest.raises(ValueError, match="La quantité doit être positive"):
            CartItem(produit_id=1, quantite=0, prix_unitaire=10.0)
        
        # Test avec prix unitaire invalide
        with pytest.raises(ValueError, match="Le prix unitaire doit être positif"):
            CartItem(produit_id=1, quantite=1, prix_unitaire=-10.0)
    
    def test_cart_item_from_dict(self):
        """Test de création d'un item à partir d'un dictionnaire"""
        data = {
            'id': 1,
            'panier_id': 1,
            'produit_id': 1,
            'quantite': 2,
            'prix_unitaire': 10.50,
            'sous_total': 21.00,
            'date_ajout': '2023-01-01T00:00:00',
            'produit': {'nom': 'Test Product'}
        }
        
        item = CartItem.from_dict(data)
        
        assert item.id == 1
        assert item.panier_id == 1
        assert item.produit_id == 1
        assert item.quantite == 2
        assert item.prix_unitaire == 10.50
        assert item.sous_total == 21.00
        assert item.produit['nom'] == 'Test Product'
    
    def test_cart_item_to_dict(self):
        """Test de conversion en dictionnaire"""
        item = CartItem(
            id=1,
            panier_id=1,
            produit_id=1,
            quantite=2,
            prix_unitaire=10.50,
            sous_total=21.00
        )
        
        data = item.to_dict()
        
        assert data['id'] == 1
        assert data['panier_id'] == 1
        assert data['produit_id'] == 1
        assert data['quantite'] == 2
        assert data['prix_unitaire'] == 10.50
        assert data['sous_total'] == 21.00


class TestCart:
    """Tests pour le modèle Cart"""
    
    def test_cart_creation(self):
        """Test de création d'un panier"""
        cart = Cart(
            id=1,
            utilisateur_id=1,
            statut='actif',
            total=50.0,
            nombre_items=3
        )
        
        assert cart.id == 1
        assert cart.utilisateur_id == 1
        assert cart.statut == 'actif'
        assert cart.total == 50.0
        assert cart.nombre_items == 3
        assert cart.items == []
    
    def test_cart_from_dict(self):
        """Test de création d'un panier à partir d'un dictionnaire"""
        data = {
            'id': 1,
            'utilisateur_id': 1,
            'statut': 'actif',
            'total': 50.0,
            'nombre_items': 2,
            'items': [
                {
                    'id': 1,
                    'produit_id': 1,
                    'quantite': 2,
                    'prix_unitaire': 10.0,
                    'sous_total': 20.0
                },
                {
                    'id': 2,
                    'produit_id': 2,
                    'quantite': 1,
                    'prix_unitaire': 30.0,
                    'sous_total': 30.0
                }
            ]
        }
        
        cart = Cart.from_dict(data)
        
        assert cart.id == 1
        assert cart.utilisateur_id == 1
        assert cart.statut == 'actif'
        assert cart.total == 50.0
        assert cart.nombre_items == 2
        assert len(cart.items) == 2
        assert cart.items[0].produit_id == 1
        assert cart.items[1].produit_id == 2
    
    def test_cart_to_dict(self):
        """Test de conversion en dictionnaire"""
        cart = Cart(
            id=1,
            utilisateur_id=1,
            statut='actif',
            total=50.0,
            nombre_items=2
        )
        
        data = cart.to_dict()
        
        assert data['id'] == 1
        assert data['utilisateur_id'] == 1
        assert data['statut'] == 'actif'
        assert data['total'] == 50.0
        assert data['nombre_items'] == 2
        assert data['items'] == []
    
    def test_cart_calculer_total(self):
        """Test de calcul du total du panier"""
        cart = Cart()
        
        # Panier vide
        assert cart.calculer_total() == 0.0
        
        # Ajouter des items
        item1 = CartItem(produit_id=1, quantite=2, prix_unitaire=10.0, sous_total=20.0)
        item2 = CartItem(produit_id=2, quantite=1, prix_unitaire=30.0, sous_total=30.0)
        
        cart.items = [item1, item2]
        
        assert cart.calculer_total() == 50.0
    
    def test_cart_calculer_nombre_items(self):
        """Test de calcul du nombre d'items"""
        cart = Cart()
        
        # Panier vide
        assert cart.calculer_nombre_items() == 0
        
        # Ajouter des items
        item1 = CartItem(produit_id=1, quantite=2, prix_unitaire=10.0, sous_total=20.0)
        item2 = CartItem(produit_id=2, quantite=3, prix_unitaire=30.0, sous_total=90.0)
        
        cart.items = [item1, item2]
        
        assert cart.calculer_nombre_items() == 5
    
    def test_cart_get_item_by_produit_id(self):
        """Test de récupération d'un item par ID de produit"""
        cart = Cart()
        
        item1 = CartItem(produit_id=1, quantite=2, prix_unitaire=10.0, sous_total=20.0)
        item2 = CartItem(produit_id=2, quantite=1, prix_unitaire=30.0, sous_total=30.0)
        
        cart.items = [item1, item2]
        
        # Item existant
        found_item = cart.get_item_by_produit_id(1)
        assert found_item is not None
        assert found_item.produit_id == 1
        
        # Item inexistant
        not_found = cart.get_item_by_produit_id(3)
        assert not_found is None
    
    def test_cart_ajouter_item(self):
        """Test d'ajout d'un item au panier"""
        cart = Cart()
        
        # Ajouter un nouvel item
        item = cart.ajouter_item(1, 2, 10.0)
        
        assert len(cart.items) == 1
        assert item.produit_id == 1
        assert item.quantite == 2
        assert item.prix_unitaire == 10.0
        assert item.sous_total == 20.0
        assert cart.total == 20.0
        assert cart.nombre_items == 2
        
        # Ajouter le même produit (doit augmenter la quantité)
        item = cart.ajouter_item(1, 1, 10.0)
        
        assert len(cart.items) == 1
        assert item.quantite == 3
        assert item.sous_total == 30.0
        assert cart.total == 30.0
        assert cart.nombre_items == 3
    
    def test_cart_supprimer_item(self):
        """Test de suppression d'un item du panier"""
        cart = Cart()
        
        item1 = CartItem(produit_id=1, quantite=2, prix_unitaire=10.0, sous_total=20.0)
        item2 = CartItem(produit_id=2, quantite=1, prix_unitaire=30.0, sous_total=30.0)
        
        cart.items = [item1, item2]
        cart.total = 50.0
        cart.nombre_items = 3
        
        # Supprimer un item existant
        success = cart.supprimer_item(1)
        
        assert success is True
        assert len(cart.items) == 1
        assert cart.items[0].produit_id == 2
        assert cart.total == 30.0
        assert cart.nombre_items == 1
        
        # Supprimer un item inexistant
        success = cart.supprimer_item(3)
        assert success is False
    
    def test_cart_modifier_quantite(self):
        """Test de modification de quantité d'un item"""
        cart = Cart()
        
        item = CartItem(produit_id=1, quantite=2, prix_unitaire=10.0, sous_total=20.0)
        cart.items = [item]
        cart.total = 20.0
        cart.nombre_items = 2
        
        # Modifier la quantité
        success = cart.modifier_quantite(1, 5)
        
        assert success is True
        assert item.quantite == 5
        assert item.sous_total == 50.0
        assert cart.total == 50.0
        assert cart.nombre_items == 5
        
        # Mettre la quantité à 0 (doit supprimer l'item)
        success = cart.modifier_quantite(1, 0)
        
        assert success is True
        assert len(cart.items) == 0
        assert cart.total == 0.0
        assert cart.nombre_items == 0
    
    def test_cart_vider(self):
        """Test de vidage du panier"""
        cart = Cart()
        
        item1 = CartItem(produit_id=1, quantite=2, prix_unitaire=10.0, sous_total=20.0)
        item2 = CartItem(produit_id=2, quantite=1, prix_unitaire=30.0, sous_total=30.0)
        
        cart.items = [item1, item2]
        cart.total = 50.0
        cart.nombre_items = 3
        
        cart.vider()
        
        assert len(cart.items) == 0
        assert cart.total == 0.0
        assert cart.nombre_items == 0


class TestCartSummary:
    """Tests pour le modèle CartSummary"""
    
    def test_cart_summary_creation(self):
        """Test de création d'un résumé de panier"""
        summary = CartSummary(
            nombre_items=3,
            total=50.0,
            items=[{'produit_id': 1, 'quantite': 2}]
        )
        
        assert summary.nombre_items == 3
        assert summary.total == 50.0
        assert len(summary.items) == 1
    
    def test_cart_summary_from_dict(self):
        """Test de création d'un résumé à partir d'un dictionnaire"""
        data = {
            'nombre_items': 2,
            'total': 30.0,
            'items': [
                {'produit_id': 1, 'quantite': 1},
                {'produit_id': 2, 'quantite': 1}
            ]
        }
        
        summary = CartSummary.from_dict(data)
        
        assert summary.nombre_items == 2
        assert summary.total == 30.0
        assert len(summary.items) == 2
    
    def test_cart_summary_to_dict(self):
        """Test de conversion en dictionnaire"""
        summary = CartSummary(
            nombre_items=1,
            total=10.0,
            items=[{'produit_id': 1, 'quantite': 1}]
        )
        
        data = summary.to_dict()
        
        assert data['nombre_items'] == 1
        assert data['total'] == 10.0
        assert len(data['items']) == 1


class TestCartRequests:
    """Tests pour les modèles de requêtes de panier"""
    
    def test_add_to_cart_request(self):
        """Test de la requête d'ajout au panier"""
        request = AddToCartRequest(produit_id=1, quantite=2)
        
        assert request.produit_id == 1
        assert request.quantite == 2
        
        data = request.to_dict()
        assert data['produit_id'] == 1
        assert data['quantite'] == 2
    
    def test_update_cart_quantity_request(self):
        """Test de la requête de modification de quantité"""
        request = UpdateCartQuantityRequest(produit_id=1, quantite=5)
        
        assert request.produit_id == 1
        assert request.quantite == 5
        
        data = request.to_dict()
        assert data['produit_id'] == 1
        assert data['quantite'] == 5
    
    def test_remove_from_cart_request(self):
        """Test de la requête de suppression du panier"""
        request = RemoveFromCartRequest(produit_id=1)
        
        assert request.produit_id == 1
        
        data = request.to_dict()
        assert data['produit_id'] == 1
