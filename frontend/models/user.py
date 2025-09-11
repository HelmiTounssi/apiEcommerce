"""
Modèle Utilisateur pour le frontend
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """Modèle Utilisateur"""
    id: Optional[int] = None
    email: str = ""
    nom: str = ""
    role: str = "client"
    date_creation: Optional[datetime] = None
    
    def __post_init__(self):
        """Validation après initialisation"""
        if not self.email:
            raise ValueError("L'email est requis")
        if not self.nom:
            raise ValueError("Le nom est requis")
        if self.role not in ["client", "admin"]:
            raise ValueError("Le rôle doit être 'client' ou 'admin'")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Crée un utilisateur à partir d'un dictionnaire"""
        return cls(
            id=data.get('id'),
            email=data.get('email', ''),
            nom=data.get('nom', ''),
            role=data.get('role', 'client'),
            date_creation=datetime.fromisoformat(data['date_creation']) if data.get('date_creation') else None
        )
    
    def to_dict(self) -> dict:
        """Convertit l'utilisateur en dictionnaire"""
        return {
            'id': self.id,
            'email': self.email,
            'nom': self.nom,
            'role': self.role,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None
        }
    
    def to_create_dict(self) -> dict:
        """Convertit en dictionnaire pour la création"""
        return {
            'email': self.email,
            'nom': self.nom,
            'role': self.role
        }
    
    def to_update_dict(self) -> dict:
        """Convertit en dictionnaire pour la mise à jour"""
        data = {}
        if self.email:
            data['email'] = self.email
        if self.nom:
            data['nom'] = self.nom
        if self.role:
            data['role'] = self.role
        return data


@dataclass
class CreateUserRequest:
    """Requête de création d'utilisateur"""
    email: str
    mot_de_passe: str
    nom: str
    role: str = "client"
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        return {
            'email': self.email,
            'mot_de_passe': self.mot_de_passe,
            'nom': self.nom,
            'role': self.role
        }


@dataclass
class UpdateUserRequest:
    """Requête de mise à jour d'utilisateur"""
    email: Optional[str] = None
    nom: Optional[str] = None
    role: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convertit en dictionnaire"""
        data = {}
        if self.email is not None:
            data['email'] = self.email
        if self.nom is not None:
            data['nom'] = self.nom
        if self.role is not None:
            data['role'] = self.role
        return data

