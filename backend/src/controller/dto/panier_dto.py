"""
DTOs pour le panier
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class PanierDTO:
    """DTO pour un panier"""
    id: Optional[int] = None
    utilisateur_id: Optional[int] = None
    session_id: Optional[str] = None
    date_creation: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    statut: str = 'actif'
    items: Optional[List['PanierItemDTO']] = None
    total: float = 0.0
    nombre_items: int = 0


@dataclass
class PanierItemDTO:
    """DTO pour un item de panier"""
    id: Optional[int] = None
    panier_id: Optional[int] = None
    produit_id: int = 0
    quantite: int = 1
    prix_unitaire: float = 0.0
    sous_total: float = 0.0
    date_ajout: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    produit: Optional[dict] = None


@dataclass
class AjouterAuPanierDTO:
    """DTO pour ajouter un produit au panier"""
    produit_id: int
    quantite: int = 1


@dataclass
class ModifierQuantiteDTO:
    """DTO pour modifier la quantité d'un produit dans le panier"""
    produit_id: int
    quantite: int


@dataclass
class SupprimerDuPanierDTO:
    """DTO pour supprimer un produit du panier"""
    produit_id: int


@dataclass
class PanierResumeDTO:
    """DTO pour le résumé du panier"""
    nombre_items: int = 0
    total: float = 0.0
    items: Optional[List[dict]] = None
