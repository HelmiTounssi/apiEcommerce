"""
Implémentation du service commande
"""

from typing import List, Optional, Dict, Any
from ...domain.models import Commande
from ...data.repositories import CommandeRepository
from ..interfaces.commande_service import ICommandeService


class CommandeService(ICommandeService):
    """Implémentation du service commande"""
    
    def __init__(self):
        self.repository = CommandeRepository()
    
    def get_all_orders(self) -> List[Commande]:
        """Récupère toutes les commandes"""
        return self.repository.get_all()
    
    def get_order_by_id(self, order_id: int) -> Optional[Commande]:
        """Récupère une commande par son ID"""
        return self.repository.get_by_id(order_id)
    
    def create_order(self, utilisateur_id: int, adresse_livraison: str, 
                    lignes_commande: List[Dict[str, Any]]) -> Commande:
        """Crée une nouvelle commande"""
        return self.repository.create_commande(utilisateur_id, adresse_livraison, lignes_commande)
    
    def update_order(self, order_id: int, **kwargs) -> Optional[Commande]:
        """Met à jour une commande"""
        return self.repository.update(order_id, **kwargs)
    
    def delete_order(self, order_id: int) -> bool:
        """Supprime une commande"""
        return self.repository.delete(order_id)
    
    def get_orders_by_user(self, user_id: int) -> List[Commande]:
        """Récupère les commandes d'un utilisateur"""
        return self.repository.get_by_utilisateur(user_id)
    
    def get_orders_by_status(self, status: str) -> List[Commande]:
        """Récupère les commandes par statut"""
        return self.repository.get_by_statut(status)
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Met à jour le statut d'une commande"""
        return self.repository.update_statut(order_id, status)
    
    def calculate_order_total(self, order_id: int) -> float:
        """Calcule le total d'une commande"""
        order = self.get_order_by_id(order_id)
        if order:
            return order.calculer_total()
        return 0.0

