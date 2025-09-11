"""
Service pour la gestion des utilisateurs
"""

from typing import List, Optional
from .base_service import BaseService
from ..models import User, CreateUserRequest, UpdateUserRequest


class UserService(BaseService):
    """Service pour la gestion des utilisateurs"""
    
    def get_all(self) -> List[User]:
        """Récupère tous les utilisateurs"""
        try:
            users_data = self.api_client.get_users()
            return [User.from_dict(user_data) for user_data in users_data]
        except Exception as e:
            self.handle_error(e, "récupération des utilisateurs")
            return []
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Récupère un utilisateur par ID"""
        try:
            user_data = self.api_client.get_user(user_id)
            return User.from_dict(user_data) if user_data else None
        except Exception as e:
            self.handle_error(e, f"récupération de l'utilisateur {user_id}")
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Récupère un utilisateur par email"""
        try:
            user_data = self.api_client.get_user_by_email(email)
            return User.from_dict(user_data) if user_data else None
        except Exception as e:
            self.handle_error(e, f"récupération de l'utilisateur {email}")
            return None
    
    def get_by_role(self, role: str) -> List[User]:
        """Récupère les utilisateurs par rôle"""
        try:
            users_data = self.api_client.get_users_by_role(role)
            return [User.from_dict(user_data) for user_data in users_data]
        except Exception as e:
            self.handle_error(e, f"récupération des utilisateurs {role}")
            return []
    
    def create(self, user_request: CreateUserRequest) -> Optional[User]:
        """Crée un nouvel utilisateur"""
        try:
            user_data = self.api_client.create_user(user_request.to_dict())
            if user_data:
                self.show_success(f"Utilisateur {user_data['nom']} créé avec succès")
                return User.from_dict(user_data)
            return None
        except Exception as e:
            self.handle_error(e, "création de l'utilisateur")
            return None
    
    def update(self, user_id: int, user_request: UpdateUserRequest) -> Optional[User]:
        """Met à jour un utilisateur"""
        try:
            user_data = self.api_client.update_user(user_id, user_request.to_dict())
            if user_data:
                self.show_success(f"Utilisateur {user_data['nom']} mis à jour avec succès")
                return User.from_dict(user_data)
            return None
        except Exception as e:
            self.handle_error(e, f"mise à jour de l'utilisateur {user_id}")
            return None
    
    def delete(self, user_id: int) -> bool:
        """Supprime un utilisateur"""
        try:
            success = self.api_client.delete_user(user_id)
            if success:
                self.show_success(f"Utilisateur {user_id} supprimé avec succès")
            else:
                self.show_warning(f"Impossible de supprimer l'utilisateur {user_id}")
            return success
        except Exception as e:
            self.handle_error(e, f"suppression de l'utilisateur {user_id}")
            return False
    
    def get_statistics(self) -> dict:
        """Récupère les statistiques des utilisateurs"""
        try:
            all_users = self.get_all()
            clients = self.get_by_role("client")
            admins = self.get_by_role("admin")
            
            return {
                "total": len(all_users),
                "clients": len(clients),
                "admins": len(admins),
                "users": all_users
            }
        except Exception as e:
            self.handle_error(e, "récupération des statistiques utilisateurs")
            return {"total": 0, "clients": 0, "admins": 0, "users": []}

