"""
Repository pour la gestion des utilisateurs
"""

from typing import List, Optional
from .base_repository import BaseRepository
from ...domain.models import Utilisateur
from ...data.database.db import db


class UtilisateurRepository(BaseRepository):
    """Repository pour la gestion des utilisateurs"""
    
    def __init__(self):
        super().__init__(Utilisateur)
    
    def get_by_email(self, email: str) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son email"""
        return Utilisateur.query.filter_by(email=email).first()
    
    def get_by_role(self, role: str) -> List[Utilisateur]:
        """Récupère tous les utilisateurs d'un rôle donné"""
        return Utilisateur.query.filter_by(role=role).all()
    
    def create_user(self, email: str, mot_de_passe: str, nom: str, role: str = 'client') -> Utilisateur:
        """Crée un nouvel utilisateur avec mot de passe haché"""
        return self.create(
            email=email,
            mot_de_passe=mot_de_passe,
            nom=nom,
            role=role
        )
    
    def authenticate(self, email: str, password: str) -> Optional[Utilisateur]:
        """Authentifie un utilisateur"""
        user = self.get_by_email(email)
        if user and user.check_password(password):
            return user
        return None

