"""
Modèle Panier pour la gestion du panier d'achat
"""

from datetime import datetime
from typing import Dict, List, Any
from ...data.database.db import db


class Panier(db.Model):
    """Modèle Panier pour la base de données"""
    
    __tablename__ = 'paniers'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=True)
    session_id = db.Column(db.String(255), nullable=True)  # Pour les utilisateurs non connectés
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    statut = db.Column(db.String(50), default='actif')  # actif, abandonne, converti
    
    # Relations
    utilisateur = db.relationship('Utilisateur', backref='paniers')
    items = db.relationship('PanierItem', backref='panier', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'session_id': self.session_id,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None,
            'statut': self.statut,
            'items': [item.to_dict() for item in self.items],
            'total': self.calculer_total(),
            'nombre_items': self.calculer_nombre_items()
        }
    
    def calculer_total(self) -> float:
        """Calcule le total du panier"""
        return sum(item.sous_total for item in self.items)
    
    def calculer_nombre_items(self) -> int:
        """Calcule le nombre total d'items dans le panier"""
        return sum(item.quantite for item in self.items)
    
    def ajouter_produit(self, produit_id: int, quantite: int = 1) -> 'PanierItem':
        """Ajoute un produit au panier"""
        # Vérifier si le produit existe déjà dans le panier
        item_existant = PanierItem.query.filter_by(
            panier_id=self.id,
            produit_id=produit_id
        ).first()
        
        if item_existant:
            # Mettre à jour la quantité
            item_existant.quantite += quantite
            item_existant.date_modification = datetime.utcnow()
        else:
            # Créer un nouvel item
            from ...domain.models.produit import Produit
            produit = Produit.query.get(produit_id)
            if not produit:
                raise ValueError(f"Produit avec l'ID {produit_id} non trouvé")
            
            item_existant = PanierItem(
                panier_id=self.id,
                produit_id=produit_id,
                quantite=quantite,
                prix_unitaire=produit.prix
            )
            db.session.add(item_existant)
        
        self.date_modification = datetime.utcnow()
        db.session.commit()
        return item_existant
    
    def supprimer_produit(self, produit_id: int) -> bool:
        """Supprime un produit du panier"""
        item = PanierItem.query.filter_by(
            panier_id=self.id,
            produit_id=produit_id
        ).first()
        
        if item:
            db.session.delete(item)
            self.date_modification = datetime.utcnow()
            db.session.commit()
            return True
        return False
    
    def modifier_quantite(self, produit_id: int, quantite: int) -> bool:
        """Modifie la quantité d'un produit dans le panier"""
        if quantite <= 0:
            return self.supprimer_produit(produit_id)
        
        item = PanierItem.query.filter_by(
            panier_id=self.id,
            produit_id=produit_id
        ).first()
        
        if item:
            item.quantite = quantite
            item.date_modification = datetime.utcnow()
            self.date_modification = datetime.utcnow()
            db.session.commit()
            return True
        return False
    
    def vider(self):
        """Vide le panier"""
        for item in self.items:
            db.session.delete(item)
        self.date_modification = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Panier {self.id} - Utilisateur {self.utilisateur_id}>'


class PanierItem(db.Model):
    """Modèle Item de panier"""
    
    __tablename__ = 'panier_items'
    
    id = db.Column(db.Integer, primary_key=True)
    panier_id = db.Column(db.Integer, db.ForeignKey('paniers.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False, default=1)
    prix_unitaire = db.Column(db.Float, nullable=False)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    produit = db.relationship('Produit', backref='panier_items')
    
    @property
    def sous_total(self) -> float:
        """Calcule le sous-total de cet item"""
        return self.quantite * self.prix_unitaire
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'panier_id': self.panier_id,
            'produit_id': self.produit_id,
            'quantite': self.quantite,
            'prix_unitaire': self.prix_unitaire,
            'sous_total': self.sous_total,
            'date_ajout': self.date_ajout.isoformat() if self.date_ajout else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None,
            'produit': self.produit.to_dict() if self.produit else None
        }
    
    def __repr__(self):
        return f'<PanierItem {self.id} - Produit {self.produit_id} - Quantité {self.quantite}>'
