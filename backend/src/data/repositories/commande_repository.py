"""
Repository pour la gestion des commandes
"""

from typing import List
from .base_repository import BaseRepository
from ...domain.models import Commande, LigneCommande


class CommandeRepository(BaseRepository):
    """Repository pour la gestion des commandes"""
    
    def __init__(self):
        super().__init__(Commande)
    
    def get_by_utilisateur(self, utilisateur_id: int) -> List[Commande]:
        """Récupère toutes les commandes d'un utilisateur"""
        return Commande.query.filter_by(utilisateur_id=utilisateur_id).all()
    
    def get_by_statut(self, statut: str) -> List[Commande]:
        """Récupère toutes les commandes d'un statut donné"""
        return Commande.query.filter_by(statut=statut).all()
    
    def update_statut(self, commande_id: int, statut: str) -> bool:
        """Met à jour le statut d'une commande"""
        commande = self.get_by_id(commande_id)
        if commande:
            commande.statut = statut
            self.model_class.query.session.commit()
            return True
        return False
    
    def create_commande(self, utilisateur_id: int, adresse_livraison: str, lignes_commande: List[dict]) -> Commande:
        """Crée une nouvelle commande avec ses lignes"""
        commande = self.create(
            utilisateur_id=utilisateur_id,
            adresse_livraison=adresse_livraison
        )
        
        # Ajouter les lignes de commande
        from .ligne_commande_repository import LigneCommandeRepository
        for ligne_data in lignes_commande:
            LigneCommandeRepository().create(
                commande_id=commande.id,
                produit_id=ligne_data['produit_id'],
                quantite=ligne_data['quantite'],
                prix_unitaire=ligne_data['prix_unitaire']
            )
        
        return commande

