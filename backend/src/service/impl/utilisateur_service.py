"""
Implémentation du service utilisateur
"""

from typing import List, Optional
from ...domain.models import Utilisateur
from ...data.repositories import UtilisateurRepository
from ..interfaces.utilisateur_service import IUtilisateurService


class UtilisateurService(IUtilisateurService):
    """Implémentation du service utilisateur"""
    
    def __init__(self):
        self.repository = UtilisateurRepository()
    
    def get_all_users(self) -> List[Utilisateur]:
        """Récupère tous les utilisateurs"""
        return self.repository.get_all()
    
    def get_user_by_id(self, user_id: int) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son ID"""
        return self.repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son email"""
        return self.repository.get_by_email(email)
    
    def create_user(self, email: str, password: str, nom: str, role: str = 'client') -> Utilisateur:
        """Crée un nouvel utilisateur"""
        return self.repository.create_user(email, password, nom, role)
    
    def update_user(self, user_id: int, **kwargs) -> Optional[Utilisateur]:
        """Met à jour un utilisateur"""
        return self.repository.update(user_id, **kwargs)
    
    def delete_user(self, user_id: int) -> bool:
        """Supprime un utilisateur"""
        return self.repository.delete(user_id)
    
    def authenticate_user(self, email: str, password: str) -> Optional[Utilisateur]:
        """Authentifie un utilisateur"""
        return self.repository.authenticate(email, password)
    
    def get_users_by_role(self, role: str) -> List[Utilisateur]:
        """Récupère les utilisateurs par rôle"""
        return self.repository.get_by_role(role)

