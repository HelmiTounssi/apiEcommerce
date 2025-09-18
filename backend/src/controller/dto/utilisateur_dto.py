"""
DTOs pour les utilisateurs
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class UtilisateurDTO:
    """DTO pour un utilisateur"""
    id: Optional[int] = None
    email: str = ""
    nom: str = ""
    role: str = "client"
    date_creation: Optional[datetime] = None


@dataclass
class CreateUtilisateurDTO:
    """DTO pour créer un utilisateur"""
    email: str
    mot_de_passe: str
    nom: str
    role: str = "client"


@dataclass
class UpdateUtilisateurDTO:
    """DTO pour mettre à jour un utilisateur"""
    email: Optional[str] = None
    nom: Optional[str] = None
    role: Optional[str] = None


@dataclass
class LoginDTO:
    """DTO pour l'authentification"""
    email: str
    mot_de_passe: str

