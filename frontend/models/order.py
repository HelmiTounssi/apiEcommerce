"""
Modèle Commande pour le frontend
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class OrderLine:
    """Modèle Ligne de Commande"""
    id: Optional[int] = None
    commande_id: Optional[int] = None
    produit_id: int = 0
    quantite: int = 0
    prix_unitaire: float = 0.0
    total_ligne: Optional[float] = None
    
    def __post_init__(self):
        """Validation après initialisation"""
        if self.produit_id <= 0:
            raise ValueError("L'ID du produit est requis")
        if self.quantite <= 0:
            raise ValueError("La quantité doit être positive")
        if self.prix_unitaire < 0:
            raise ValueError("Le prix unitaire doit être positif")
        
        # Calculer le total de la ligne
        if self.total_ligne is None:
            self.total_ligne = self.quantite * self.prix_unitaire
    
    @classmethod
    def from_dict(cls, data: dict) -> 'OrderLine':
        """Crée une ligne de commande à partir d'un dictionnaire"""
        return cls(
            id=data.get('id'),
            commande_id=data.get('commande_id'),
            produit_id=int(data.get('produit_id', 0)),
            quantite=int(data.get('quantite', 0)),
            prix_unitaire=float(data.get('prix_unitaire', 0)),
            total_ligne=float(data.get('total_ligne', 0)) if data.get('total_ligne') else None
        )
    
    def to_dict(self) -> dict:
        """Convertit la ligne de commande en dictionnaire"""
        return {
            'id': self.id,
            'commande_id': self.commande_id,
            'produit_id': self.produit_id,
            'quantite': self.quantite,
            'prix_unitaire': self.prix_unitaire,
            'total_ligne': self.total_ligne
        }


@dataclass
class Order:
    """Modèle Commande"""
    id: Optional[int] = None
    utilisateur_id: int = 0
    date_commande: Optional[datetime] = None
    adresse_livraison: str = ""
    statut: str = "en_attente"
    lignes_commande: List[OrderLine] = None
    total: Optional[float] = None
    
    def __post_init__(self):
        """Validation après initialisation"""
        if self.utilisateur_id <= 0:
            raise ValueError("L'ID de l'utilisateur est requis")
        if not self.adresse_livraison:
            raise ValueError("L'adresse de livraison est requise")
        if self.statut not in ["en_attente", "validée", "expédiée", "annulée"]:
            raise ValueError("Statut invalide")
        
        if self.lignes_commande is None:
            self.lignes_commande = []
        
        # Calculer le total
        if self.total is None and self.lignes_commande:
            self.total = sum(ligne.total_ligne or 0 for ligne in self.lignes_commande)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        """Crée une commande à partir d'un dictionnaire"""
        lignes = []
        if data.get('lignes_commande'):
            lignes = [OrderLine.from_dict(ligne) for ligne in data['lignes_commande']]
        
        return cls(
            id=data.get('id'),
            utilisateur_id=int(data.get('utilisateur_id', 0)),
            date_commande=datetime.fromisoformat(data['date_commande']) if data.get('date_commande') else None,
            adresse_livraison=data.get('adresse_livraison', ''),
            statut=data.get('statut', 'en_attente'),
            lignes_commande=lignes,
            total=float(data.get('total', 0)) if data.get('total') else None
        )
    
    def to_dict(self) -> dict:
        """Convertit la commande en dictionnaire"""
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'date_commande': self.date_commande.isoformat() if self.date_commande else None,
            'adresse_livraison': self.adresse_livraison,
            'statut': self.statut,
            'lignes_commande': [ligne.to_dict() for ligne in self.lignes_commande],
            'total': self.total
        }
    
    def to_create_dict(self) -> dict:
        """Convertit en dictionnaire pour la création"""
        return {
            'utilisateur_id': self.utilisateur_id,
            'adresse_livraison': self.adresse_livraison,
            'statut': self.statut,
            'lignes_commande': [ligne.to_dict() for ligne in self.lignes_commande]
        }
    
    def to_update_dict(self) -> dict:
        """Convertit en dictionnaire pour la mise à jour"""
        data = {}
        if self.adresse_livraison:
            data['adresse_livraison'] = self.adresse_livraison
        if self.statut:
            data['statut'] = self.statut
        return data


@dataclass
class CreateOrderRequest:
    """Requête de création de commande"""
    utilisateur_id: int
    adresse_livraison: str
    statut: str = "en_attente"
    lignes_commande: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.lignes_commande is None:
            self.lignes_commande = []
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            'utilisateur_id': self.utilisateur_id,
            'adresse_livraison': self.adresse_livraison,
            'statut': self.statut,
            'lignes_commande': self.lignes_commande
        }


@dataclass
class UpdateOrderRequest:
    """Requête de mise à jour de commande"""
    adresse_livraison: Optional[str] = None
    statut: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        data = {}
        if self.adresse_livraison is not None:
            data['adresse_livraison'] = self.adresse_livraison
        if self.statut is not None:
            data['statut'] = self.statut
        return data


@dataclass
class UpdateOrderStatusRequest:
    """Requête de mise à jour du statut de commande"""
    statut: str
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {'statut': self.statut}

