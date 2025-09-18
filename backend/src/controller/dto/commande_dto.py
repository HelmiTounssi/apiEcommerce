"""
DTOs pour les commandes
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class LigneCommandeDTO:
    """DTO pour une ligne de commande"""
    id: Optional[int] = None
    commande_id: Optional[int] = None
    produit_id: int = 0
    quantite: int = 0
    prix_unitaire: float = 0.0
    total_ligne: Optional[float] = None


@dataclass
class CommandeDTO:
    """DTO pour une commande"""
    id: Optional[int] = None
    utilisateur_id: int = 0
    date_commande: Optional[datetime] = None
    adresse_livraison: str = ""
    statut: str = "en_attente"
    lignes_commande: List[LigneCommandeDTO] = None
    total: Optional[float] = None


@dataclass
class CreateCommandeDTO:
    """DTO pour créer une commande"""
    utilisateur_id: int
    adresse_livraison: str
    statut: str = "en_attente"
    lignes_commande: List[Dict[str, Any]] = None


@dataclass
class UpdateCommandeDTO:
    """DTO pour mettre à jour une commande"""
    adresse_livraison: Optional[str] = None
    statut: Optional[str] = None


@dataclass
class CreateLigneCommandeDTO:
    """DTO pour créer une ligne de commande"""
    commande_id: int
    produit_id: int
    quantite: int
    prix_unitaire: float


@dataclass
class UpdateLigneCommandeDTO:
    """DTO pour mettre à jour une ligne de commande"""
    quantite: Optional[int] = None
    prix_unitaire: Optional[float] = None

