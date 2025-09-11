"""
Modèle Produit
"""

from datetime import datetime
from ...data.database.db import db


class Produit(db.Model):
    """Modèle Produit pour la base de données"""
    
    __tablename__ = 'produits'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    categorie = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    quantite_stock = db.Column(db.Integer, nullable=False, default=0)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    lignes_commande = db.relationship('LigneCommande', backref='produit', lazy=True)
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'categorie': self.categorie,
            'prix': self.prix,
            'quantite_stock': self.quantite_stock,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None
        }
    
    def __repr__(self):
        return f'<Produit {self.nom}>'

