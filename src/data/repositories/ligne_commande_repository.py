"""
Repository pour la gestion des lignes de commande
"""

from typing import List
from .base_repository import BaseRepository
from ...domain.models import LigneCommande


class LigneCommandeRepository(BaseRepository):
    """Repository pour la gestion des lignes de commande"""
    
    def __init__(self):
        super().__init__(LigneCommande)
    
    def get_by_commande(self, commande_id: int) -> List[LigneCommande]:
        """Récupère toutes les lignes d'une commande"""
        return LigneCommande.query.filter_by(commande_id=commande_id).all()
    
    def get_by_produit(self, produit_id: int) -> List[LigneCommande]:
        """Récupère toutes les lignes pour un produit"""
        return LigneCommande.query.filter_by(produit_id=produit_id).all()
    
    def get_total_ventes_produit(self, produit_id: int) -> int:
        """Calcule le total des ventes d'un produit"""
        lignes = self.get_by_produit(produit_id)
        return sum(ligne.quantite for ligne in lignes)

