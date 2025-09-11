"""
DTOs pour les produits
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ProduitDTO:
    """DTO pour un produit"""
    id: Optional[int] = None
    nom: str = ""
    description: Optional[str] = None
    categorie: str = ""
    prix: float = 0.0
    quantite_stock: int = 0
    date_creation: Optional[datetime] = None


@dataclass
class CreateProduitDTO:
    """DTO pour créer un produit"""
    nom: str
    description: Optional[str] = None
    categorie: str = ""
    prix: float = 0.0
    quantite_stock: int = 0


@dataclass
class UpdateProduitDTO:
    """DTO pour mettre à jour un produit"""
    nom: Optional[str] = None
    description: Optional[str] = None
    categorie: Optional[str] = None
    prix: Optional[float] = None
    quantite_stock: Optional[int] = None


@dataclass
class UpdateStockDTO:
    """DTO pour mettre à jour le stock"""
    quantite: int

