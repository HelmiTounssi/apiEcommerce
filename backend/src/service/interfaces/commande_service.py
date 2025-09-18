"""
Interface du service commande
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ...domain.models import Commande


class ICommandeService(ABC):
    """Interface du service commande"""
    
    @abstractmethod
    def get_all_orders(self) -> List[Commande]:
        """Récupère toutes les commandes"""
        pass
    
    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Optional[Commande]:
        """Récupère une commande par son ID"""
        pass
    
    @abstractmethod
    def create_order(self, utilisateur_id: int, adresse_livraison: str, 
                    lignes_commande: List[Dict[str, Any]]) -> Commande:
        """Crée une nouvelle commande"""
        pass
    
    @abstractmethod
    def update_order(self, order_id: int, **kwargs) -> Optional[Commande]:
        """Met à jour une commande"""
        pass
    
    @abstractmethod
    def delete_order(self, order_id: int) -> bool:
        """Supprime une commande"""
        pass
    
    @abstractmethod
    def get_orders_by_user(self, user_id: int) -> List[Commande]:
        """Récupère les commandes d'un utilisateur"""
        pass
    
    @abstractmethod
    def get_orders_by_status(self, status: str) -> List[Commande]:
        """Récupère les commandes par statut"""
        pass
    
    @abstractmethod
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Met à jour le statut d'une commande"""
        pass
    
    @abstractmethod
    def calculate_order_total(self, order_id: int) -> float:
        """Calcule le total d'une commande"""
        pass

