"""
Implémentation du service produit
"""

from typing import List, Optional
from ...domain.models import Produit
from ...data.repositories import ProduitRepository
from ..interfaces.produit_service import IProduitService


class ProduitService(IProduitService):
    """Implémentation du service produit"""
    
    def __init__(self):
        self.repository = ProduitRepository()
    
    def get_all_products(self) -> List[Produit]:
        """Récupère tous les produits"""
        return self.repository.get_all()
    
    def get_product_by_id(self, product_id: int) -> Optional[Produit]:
        """Récupère un produit par son ID"""
        return self.repository.get_by_id(product_id)
    
    def create_product(self, nom: str, description: str, categorie: str, 
                      prix: float, quantite_stock: int = 0) -> Produit:
        """Crée un nouveau produit"""
        return self.repository.create(
            nom=nom,
            description=description,
            categorie=categorie,
            prix=prix,
            quantite_stock=quantite_stock
        )
    
    def update_product(self, product_id: int, **kwargs) -> Optional[Produit]:
        """Met à jour un produit"""
        return self.repository.update(product_id, **kwargs)
    
    def delete_product(self, product_id: int) -> bool:
        """Supprime un produit"""
        return self.repository.delete(product_id)
    
    def get_products_by_category(self, category: str) -> List[Produit]:
        """Récupère les produits par catégorie"""
        return self.repository.get_by_categorie(category)
    
    def get_products_by_price_range(self, min_price: float, max_price: float) -> List[Produit]:
        """Récupère les produits par fourchette de prix"""
        return self.repository.get_by_prix_range(min_price, max_price)
    
    def get_products_in_stock(self) -> List[Produit]:
        """Récupère les produits en stock"""
        return self.repository.get_en_stock()
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Met à jour le stock d'un produit"""
        return self.repository.update_stock(product_id, quantity)
    
    def decrement_stock(self, product_id: int, quantity: int) -> bool:
        """Décrémente le stock d'un produit"""
        return self.repository.decrementer_stock(product_id, quantity)

