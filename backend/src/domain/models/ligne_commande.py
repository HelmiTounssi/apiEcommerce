"""
Modèle LigneCommande
"""

from ...data.database.db import db


class LigneCommande(db.Model):
    """Modèle LigneCommande pour la base de données"""
    
    __tablename__ = 'lignes_commande'
    
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commandes.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produits.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'commande_id': self.commande_id,
            'produit_id': self.produit_id,
            'quantite': self.quantite,
            'prix_unitaire': self.prix_unitaire,
            'total_ligne': self.quantite * self.prix_unitaire
        }
    
    def __repr__(self):
        return f'<LigneCommande {self.id} - {self.quantite}x>'

