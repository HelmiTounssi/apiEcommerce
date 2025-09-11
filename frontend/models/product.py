"""
Modèle Produit pour le frontend
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """Modèle Produit"""
    id: Optional[int] = None
    nom: str = ""
    description: Optional[str] = None
    categorie: str = ""
    prix: float = 0.0
    quantite_stock: int = 0
    date_creation: Optional[datetime] = None
    
    def __post_init__(self):
        """Validation après initialisation"""
        if not self.nom:
            raise ValueError("Le nom est requis")
        if not self.categorie:
            raise ValueError("La catégorie est requise")
        if self.prix < 0:
            raise ValueError("Le prix doit être positif")
        if self.quantite_stock < 0:
            raise ValueError("La quantité en stock doit être positive")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Crée un produit à partir d'un dictionnaire"""
        return cls(
            id=data.get('id'),
            nom=data.get('nom', ''),
            description=data.get('description'),
            categorie=data.get('categorie', ''),
            prix=float(data.get('prix', 0)),
            quantite_stock=int(data.get('quantite_stock', 0)),
            date_creation=datetime.fromisoformat(data['date_creation']) if data.get('date_creation') else None
        )
    
    def to_dict(self) -> dict:
        """Convertit le produit en dictionnaire"""
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'categorie': self.categorie,
            'prix': self.prix,
            'quantite_stock': self.quantite_stock,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None
        }
    
    def to_create_dict(self) -> dict:
        """Convertit en dictionnaire pour la création"""
        return {
            'nom': self.nom,
            'description': self.description,
            'categorie': self.categorie,
            'prix': self.prix,
            'quantite_stock': self.quantite_stock
        }
    
    def to_update_dict(self) -> dict:
        """Convertit en dictionnaire pour la mise à jour"""
        data = {}
        if self.nom:
            data['nom'] = self.nom
        if self.description is not None:
            data['description'] = self.description
        if self.categorie:
            data['categorie'] = self.categorie
        if self.prix >= 0:
            data['prix'] = self.prix
        if self.quantite_stock >= 0:
            data['quantite_stock'] = self.quantite_stock
        return data


@dataclass
class CreateProductRequest:
    """Requête de création de produit"""
    nom: str
    description: Optional[str] = None
    categorie: str = ""
    prix: float = 0.0
    quantite_stock: int = 0
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            'nom': self.nom,
            'description': self.description,
            'categorie': self.categorie,
            'prix': self.prix,
            'quantite_stock': self.quantite_stock
        }


@dataclass
class UpdateProductRequest:
    """Requête de mise à jour de produit"""
    nom: Optional[str] = None
    description: Optional[str] = None
    categorie: Optional[str] = None
    prix: Optional[float] = None
    quantite_stock: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        data = {}
        if self.nom is not None:
            data['nom'] = self.nom
        if self.description is not None:
            data['description'] = self.description
        if self.categorie is not None:
            data['categorie'] = self.categorie
        if self.prix is not None:
            data['prix'] = self.prix
        if self.quantite_stock is not None:
            data['quantite_stock'] = self.quantite_stock
        return data


@dataclass
class UpdateStockRequest:
    """Requête de mise à jour du stock"""
    quantite: int
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {'quantite': self.quantite}

