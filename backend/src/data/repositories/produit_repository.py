"""
Repository pour la gestion des produits
"""

from typing import List
from .base_repository import BaseRepository
from ...domain.models import Produit
from ...data.database.db import db


class ProduitRepository(BaseRepository):
    """Repository pour la gestion des produits"""
    
    def __init__(self):
        super().__init__(Produit)
    
    def get_by_categorie(self, categorie: str) -> List[Produit]:
        """Récupère tous les produits d'une catégorie"""
        return Produit.query.filter_by(categorie=categorie).all()
    
    def get_by_prix_range(self, prix_min: float, prix_max: float) -> List[Produit]:
        """Récupère les produits dans une fourchette de prix"""
        return Produit.query.filter(
            Produit.prix >= prix_min,
            Produit.prix <= prix_max
        ).all()
    
    def get_en_stock(self) -> List[Produit]:
        """Récupère tous les produits en stock"""
        return Produit.query.filter(Produit.quantite_stock > 0).all()
    
    def update_stock(self, produit_id: int, quantite: int) -> bool:
        """Met à jour le stock d'un produit"""
        produit = self.get_by_id(produit_id)
        if produit:
            produit.quantite_stock = quantite
            db.session.commit()
            return True
        return False
    
    def decrementer_stock(self, produit_id: int, quantite: int) -> bool:
        """Décrémente le stock d'un produit"""
        produit = self.get_by_id(produit_id)
        if produit and produit.quantite_stock >= quantite:
            produit.quantite_stock -= quantite
            db.session.commit()
            return True
        return False

