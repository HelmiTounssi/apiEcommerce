"""
Modèles Panier pour le frontend
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class CartItem:
    """Modèle Item de panier"""
    id: Optional[int] = None
    panier_id: Optional[int] = None
    produit_id: int = 0
    quantite: int = 1
    prix_unitaire: float = 0.0
    sous_total: float = 0.0
    date_ajout: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    produit: Optional[dict] = None
    
    def __post_init__(self):
        """Validation après initialisation"""
        if self.produit_id <= 0:
            raise ValueError("L'ID du produit est requis")
        if self.quantite <= 0:
            raise ValueError("La quantité doit être positive")
        if self.prix_unitaire < 0:
            raise ValueError("Le prix unitaire doit être positif")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CartItem':
        """Crée un item de panier à partir d'un dictionnaire"""
        from utils.product_utils import parse_product_data
        
        # Parser le produit s'il est une chaîne JSON
        produit = parse_product_data(data.get('produit'))
        
        return cls(
            id=data.get('id'),
            panier_id=data.get('panier_id'),
            produit_id=data.get('produit_id', 0),
            quantite=data.get('quantite', 1),
            prix_unitaire=float(data.get('prix_unitaire', 0)),
            sous_total=float(data.get('sous_total', 0)),
            date_ajout=datetime.fromisoformat(data['date_ajout']) if data.get('date_ajout') else None,
            date_modification=datetime.fromisoformat(data['date_modification']) if data.get('date_modification') else None,
            produit=produit
        )
    
    def to_dict(self) -> dict:
        """Convertit l'item en dictionnaire"""
        return {
            'id': self.id,
            'panier_id': self.panier_id,
            'produit_id': self.produit_id,
            'quantite': self.quantite,
            'prix_unitaire': self.prix_unitaire,
            'sous_total': self.sous_total,
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None,
            'produit': self.produit
        }


@dataclass
class Cart:
    """Modèle Panier"""
    id: Optional[int] = None
    utilisateur_id: Optional[int] = None
    session_id: Optional[str] = None
    date_creation: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    statut: str = 'actif'
    items: Optional[List[CartItem]] = None
    total: float = 0.0
    nombre_items: int = 0
    
    def __post_init__(self):
        """Validation après initialisation"""
        if self.items is None:
            self.items = []
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Cart':
        """Crée un panier à partir d'un dictionnaire"""
        items = []
        if data.get('items'):
            items = [CartItem.from_dict(item) for item in data['items']]
        
        return cls(
            id=data.get('id'),
            utilisateur_id=data.get('utilisateur_id'),
            session_id=data.get('session_id'),
            date_creation=datetime.fromisoformat(data['date_creation']) if data.get('date_creation') else None,
            date_modification=datetime.fromisoformat(data['date_modification']) if data.get('date_modification') else None,
            statut=data.get('statut', 'actif'),
            items=items,
            total=float(data.get('total', 0)),
            nombre_items=int(data.get('nombre_items', 0))
        )
    
    def to_dict(self) -> dict:
        """Convertit le panier en dictionnaire"""
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'session_id': self.session_id,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None,
            'statut': self.statut,
            'items': [item.to_dict() for item in self.items] if self.items else [],
            'total': self.total,
            'nombre_items': self.nombre_items
        }
    
    def calculer_total(self) -> float:
        """Calcule le total du panier"""
        if not self.items:
            return 0.0
        return sum(item.sous_total for item in self.items)
    
    def calculer_nombre_items(self) -> int:
        """Calcule le nombre total d'items dans le panier"""
        if not self.items:
            return 0
        return sum(item.quantite for item in self.items)
    
    def get_item_by_produit_id(self, produit_id: int) -> Optional[CartItem]:
        """Récupère un item par ID de produit"""
        if not self.items:
            return None
        for item in self.items:
            if item.produit_id == produit_id:
                return item
        return None
    
    def ajouter_item(self, produit_id: int, quantite: int = 1, prix_unitaire: float = 0.0) -> CartItem:
        """Ajoute un item au panier"""
        item_existant = self.get_item_by_produit_id(produit_id)
        
        if item_existant:
            # Mettre à jour la quantité
            item_existant.quantite += quantite
            item_existant.sous_total = item_existant.quantite * item_existant.prix_unitaire
        else:
            # Créer un nouvel item
            item_existant = CartItem(
                produit_id=produit_id,
                quantite=quantite,
                prix_unitaire=prix_unitaire,
                sous_total=quantite * prix_unitaire
            )
            self.items.append(item_existant)
        
        # Mettre à jour les totaux
        self.total = self.calculer_total()
        self.nombre_items = self.calculer_nombre_items()
        
        return item_existant
    
    def supprimer_item(self, produit_id: int) -> bool:
        """Supprime un item du panier"""
        if not self.items:
            return False
        
        for i, item in enumerate(self.items):
            if item.produit_id == produit_id:
                del self.items[i]
                # Mettre à jour les totaux
                self.total = self.calculer_total()
                self.nombre_items = self.calculer_nombre_items()
                return True
        
        return False
    
    def modifier_quantite(self, produit_id: int, quantite: int) -> bool:
        """Modifie la quantité d'un item"""
        if quantite <= 0:
            return self.supprimer_item(produit_id)
        
        item = self.get_item_by_produit_id(produit_id)
        if item:
            item.quantite = quantite
            item.sous_total = item.quantite * item.prix_unitaire
            # Mettre à jour les totaux
            self.total = self.calculer_total()
            self.nombre_items = self.calculer_nombre_items()
            return True
        
        return False
    
    def vider(self):
        """Vide le panier"""
        self.items = []
        self.total = 0.0
        self.nombre_items = 0


@dataclass
class AddToCartRequest:
    """Requête d'ajout au panier"""
    produit_id: int
    quantite: int = 1
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            'produit_id': self.produit_id,
            'quantite': self.quantite
        }


@dataclass
class UpdateCartQuantityRequest:
    """Requête de modification de quantité"""
    produit_id: int
    quantite: int
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            'produit_id': self.produit_id,
            'quantite': self.quantite
        }


@dataclass
class RemoveFromCartRequest:
    """Requête de suppression du panier"""
    produit_id: int
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            'produit_id': self.produit_id
        }


@dataclass
class CartSummary:
    """Résumé du panier"""
    nombre_items: int = 0
    total: float = 0.0
    items: Optional[List[dict]] = None
    
    def __post_init__(self):
        """Validation après initialisation"""
        if self.items is None:
            self.items = []
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CartSummary':
        """Crée un résumé à partir d'un dictionnaire"""
        return cls(
            nombre_items=int(data.get('nombre_items', 0)),
            total=float(data.get('total', 0)),
            items=data.get('items', [])
        )
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            'nombre_items': self.nombre_items,
            'total': self.total,
            'items': self.items or []
        }
