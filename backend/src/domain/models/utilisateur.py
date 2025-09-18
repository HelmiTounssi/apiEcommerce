"""
Modèle Utilisateur
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ...data.database.db import db


class Utilisateur(db.Model):
    """Modèle Utilisateur pour la base de données"""
    
    __tablename__ = 'utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    commandes = db.relationship('Commande', backref='utilisateur', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, email, mot_de_passe, nom, role='client'):
        self.email = email
        self.set_password(mot_de_passe)
        self.nom = nom
        self.role = role
    
    def set_password(self, password):
        """Hache le mot de passe"""
        self.mot_de_passe = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.mot_de_passe, password)
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'email': self.email,
            'nom': self.nom,
            'role': self.role,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None
        }
    
    def __repr__(self):
        return f'<Utilisateur {self.email}>'

