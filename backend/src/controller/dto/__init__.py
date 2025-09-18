"""
DTOs (Data Transfer Objects)
"""

from .utilisateur_dto import (
    UtilisateurDTO, CreateUtilisateurDTO, UpdateUtilisateurDTO, LoginDTO
)
from .produit_dto import (
    ProduitDTO, CreateProduitDTO, UpdateProduitDTO, UpdateStockDTO
)
from .commande_dto import (
    CommandeDTO, CreateCommandeDTO, UpdateCommandeDTO,
    LigneCommandeDTO, CreateLigneCommandeDTO, UpdateLigneCommandeDTO
)

__all__ = [
    # Utilisateur DTOs
    'UtilisateurDTO', 'CreateUtilisateurDTO', 'UpdateUtilisateurDTO', 'LoginDTO',
    # Produit DTOs
    'ProduitDTO', 'CreateProduitDTO', 'UpdateProduitDTO', 'UpdateStockDTO',
    # Commande DTOs
    'CommandeDTO', 'CreateCommandeDTO', 'UpdateCommandeDTO',
    'LigneCommandeDTO', 'CreateLigneCommandeDTO', 'UpdateLigneCommandeDTO'
]