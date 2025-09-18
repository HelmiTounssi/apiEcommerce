"""
Interface du service produit
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ...domain.models import Produit


class IProduitService(ABC):
    """Interface du service produit"""
    
    @abstractmethod
    def get_all_products(self) -> List[Produit]:
        """Récupère tous les produits"""
        pass
    
    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Produit]:
        """Récupère un produit par son ID"""
        pass
    
    @abstractmethod
    def create_product(self, nom: str, description: str, categorie: str, 
                      prix: float, quantite_stock: int = 0) -> Produit:
        """Crée un nouveau produit"""
        pass
    
    @abstractmethod
    def update_product(self, product_id: int, **kwargs) -> Optional[Produit]:
        """Met à jour un produit"""
        pass
    
    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        """Supprime un produit"""
        pass
    
    @abstractmethod
    def get_products_by_category(self, category: str) -> List[Produit]:
        """Récupère les produits par catégorie"""
        pass
    
    @abstractmethod
    def get_products_by_price_range(self, min_price: float, max_price: float) -> List[Produit]:
        """Récupère les produits par fourchette de prix"""
        pass
    
    @abstractmethod
    def get_products_in_stock(self) -> List[Produit]:
        """Récupère les produits en stock"""
        pass
    
    @abstractmethod
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Met à jour le stock d'un produit"""
        pass
    
    @abstractmethod
    def decrement_stock(self, product_id: int, quantity: int) -> bool:
        """Décrémente le stock d'un produit"""
        pass

