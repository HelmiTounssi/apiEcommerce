"""
Interface du service utilisateur
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ...domain.models import Utilisateur


class IUtilisateurService(ABC):
    """Interface du service utilisateur"""
    
    @abstractmethod
    def get_all_users(self) -> List[Utilisateur]:
        """Récupère tous les utilisateurs"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son ID"""
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son email"""
        pass
    
    @abstractmethod
    def create_user(self, email: str, password: str, nom: str, role: str = 'client') -> Utilisateur:
        """Crée un nouvel utilisateur"""
        pass
    
    @abstractmethod
    def update_user(self, user_id: int, **kwargs) -> Optional[Utilisateur]:
        """Met à jour un utilisateur"""
        pass
    
    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        """Supprime un utilisateur"""
        pass
    
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> Optional[Utilisateur]:
        """Authentifie un utilisateur"""
        pass
    
    @abstractmethod
    def get_users_by_role(self, role: str) -> List[Utilisateur]:
        """Récupère les utilisateurs par rôle"""
        pass

