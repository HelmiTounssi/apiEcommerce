"""
Interfaces des services
"""

from .utilisateur_service import IUtilisateurService
from .produit_service import IProduitService
from .commande_service import ICommandeService

__all__ = [
    'IUtilisateurService',
    'IProduitService',
    'ICommandeService'
]