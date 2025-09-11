"""
Modèle Commande
"""

from datetime import datetime
from ...data.database.db import db


class Commande(db.Model):
    """Modèle Commande pour la base de données"""
    
    __tablename__ = 'commandes'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    date_commande = db.Column(db.DateTime, default=datetime.utcnow)
    adresse_livraison = db.Column(db.String(500), nullable=False)
    statut = db.Column(db.String(20), nullable=False, default='en_attente')
    
    # Relations
    lignes_commande = db.relationship('LigneCommande', backref='commande', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur_id,
            'date_commande': self.date_commande.isoformat() if self.date_commande else None,
            'adresse_livraison': self.adresse_livraison,
            'statut': self.statut,
            'lignes_commande': [ligne.to_dict() for ligne in self.lignes_commande]
        }
    
    def calculer_total(self):
        """Calcule le total de la commande"""
        total = 0
        for ligne in self.lignes_commande:
            total += ligne.quantite * ligne.prix_unitaire
        return total
    
    def __repr__(self):
        return f'<Commande {self.id} - {self.statut}>'

