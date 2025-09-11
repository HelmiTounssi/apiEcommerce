"""
Service pour la gestion des commandes
"""

from typing import List, Optional
from .base_service import BaseService
from ..models import Order, CreateOrderRequest, UpdateOrderRequest, UpdateOrderStatusRequest


class OrderService(BaseService):
    """Service pour la gestion des commandes"""
    
    def get_all(self) -> List[Order]:
        """Récupère toutes les commandes"""
        try:
            orders_data = self.api_client.get_orders()
            return [Order.from_dict(order_data) for order_data in orders_data]
        except Exception as e:
            self.handle_error(e, "récupération des commandes")
            return []
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Récupère une commande par ID"""
        try:
            order_data = self.api_client.get_order(order_id)
            return Order.from_dict(order_data) if order_data else None
        except Exception as e:
            self.handle_error(e, f"récupération de la commande {order_id}")
            return None
    
    def get_by_user(self, user_id: int) -> List[Order]:
        """Récupère les commandes d'un utilisateur"""
        try:
            orders_data = self.api_client.get_orders_by_user(user_id)
            return [Order.from_dict(order_data) for order_data in orders_data]
        except Exception as e:
            self.handle_error(e, f"récupération des commandes de l'utilisateur {user_id}")
            return []
    
    def get_by_status(self, status: str) -> List[Order]:
        """Récupère les commandes par statut"""
        try:
            orders_data = self.api_client.get_orders_by_status(status)
            return [Order.from_dict(order_data) for order_data in orders_data]
        except Exception as e:
            self.handle_error(e, f"récupération des commandes {status}")
            return []
    
    def create(self, order_request: CreateOrderRequest) -> Optional[Order]:
        """Crée une nouvelle commande"""
        try:
            order_data = self.api_client.create_order(order_request.to_dict())
            if order_data:
                self.show_success(f"Commande {order_data['id']} créée avec succès")
                return Order.from_dict(order_data)
            return None
        except Exception as e:
            self.handle_error(e, "création de la commande")
            return None
    
    def update(self, order_id: int, order_request: UpdateOrderRequest) -> Optional[Order]:
        """Met à jour une commande"""
        try:
            order_data = self.api_client.update_order(order_id, order_request.to_dict())
            if order_data:
                self.show_success(f"Commande {order_data['id']} mise à jour avec succès")
                return Order.from_dict(order_data)
            return None
        except Exception as e:
            self.handle_error(e, f"mise à jour de la commande {order_id}")
            return None
    
    def delete(self, order_id: int) -> bool:
        """Supprime une commande"""
        try:
            success = self.api_client.delete_order(order_id)
            if success:
                self.show_success(f"Commande {order_id} supprimée avec succès")
            else:
                self.show_warning(f"Impossible de supprimer la commande {order_id}")
            return success
        except Exception as e:
            self.handle_error(e, f"suppression de la commande {order_id}")
            return False
    
    def update_status(self, order_id: int, status: str) -> bool:
        """Met à jour le statut d'une commande"""
        try:
            success = self.api_client.update_order_status(order_id, status)
            if success:
                self.show_success(f"Statut de la commande {order_id} mis à jour")
            else:
                self.show_warning(f"Impossible de mettre à jour le statut de la commande {order_id}")
            return success
        except Exception as e:
            self.handle_error(e, f"mise à jour du statut de la commande {order_id}")
            return False
    
    def get_total(self, order_id: int) -> Optional[float]:
        """Calcule le total d'une commande"""
        try:
            total = self.api_client.get_order_total(order_id)
            return total
        except Exception as e:
            self.handle_error(e, f"calcul du total de la commande {order_id}")
            return None
    
    def get_statistics(self) -> dict:
        """Récupère les statistiques des commandes"""
        try:
            all_orders = self.get_all()
            
            # Statistiques par statut
            status_stats = {}
            for order in all_orders:
                if order.statut not in status_stats:
                    status_stats[order.statut] = 0
                status_stats[order.statut] += 1
            
            # Chiffre d'affaires total
            total_revenue = sum(order.total or 0 for order in all_orders)
            
            # Nombre moyen d'articles par commande
            total_items = sum(len(order.lignes_commande) for order in all_orders)
            avg_items = total_items / len(all_orders) if all_orders else 0
            
            return {
                "total": len(all_orders),
                "status_stats": status_stats,
                "total_revenue": total_revenue,
                "avg_items_per_order": avg_items,
                "orders": all_orders
            }
        except Exception as e:
            self.handle_error(e, "récupération des statistiques commandes")
            return {
                "total": 0, "status_stats": {}, "total_revenue": 0, 
                "avg_items_per_order": 0, "orders": []
            }

