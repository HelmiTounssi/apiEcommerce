"""
Service pour les statistiques
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from ...data.repositories.utilisateur_repository import UtilisateurRepository
from ...data.repositories.produit_repository import ProduitRepository
from ...data.repositories.commande_repository import CommandeRepository
from ...data.repositories.ligne_commande_repository import LigneCommandeRepository
from ...data.database.db import db

class StatsService:
    """Service pour les statistiques du système"""
    
    def __init__(self):
        self.user_repo = UtilisateurRepository()
        self.product_repo = ProduitRepository()
        self.order_repo = CommandeRepository()
        self.line_repo = LigneCommandeRepository()
    
    def get_general_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques générales"""
        try:
            today = datetime.now().date()
            
            # Statistiques des utilisateurs
            user_stats = self.get_user_stats()
            
            # Statistiques des produits
            product_stats = self.get_product_stats()
            
            # Statistiques des commandes
            order_stats = self.get_order_stats()
            
            # Statistiques du chiffre d'affaires
            revenue_stats = self.get_revenue_stats()
            
            return {
                'users': user_stats,
                'products': product_stats,
                'orders': order_stats,
                'revenue': revenue_stats,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques générales: {str(e)}")
    
    def get_user_stats(self) -> Dict[str, int]:
        """Récupère les statistiques des utilisateurs"""
        try:
            today = datetime.now().date()
            
            # Total des utilisateurs
            total_users = self.user_repo.count()
            
            # Nouveaux utilisateurs aujourd'hui
            new_today = self.user_repo.count_by_date(today)
            
            # Utilisateurs actifs (ayant passé une commande dans les 30 derniers jours)
            active_date = today - timedelta(days=30)
            active_users = self.user_repo.count_active_since(active_date)
            
            return {
                'total': total_users,
                'new_today': new_today,
                'active': active_users
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques utilisateurs: {str(e)}")
    
    def get_product_stats(self) -> Dict[str, int]:
        """Récupère les statistiques des produits"""
        try:
            today = datetime.now().date()
            
            # Total des produits
            total_products = self.product_repo.count()
            
            # Nouveaux produits aujourd'hui
            new_today = self.product_repo.count_by_date(today)
            
            # Produits en rupture de stock
            low_stock = self.product_repo.count_low_stock()
            
            return {
                'total': total_products,
                'new_today': new_today,
                'low_stock': low_stock
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques produits: {str(e)}")
    
    def get_order_stats(self) -> Dict[str, int]:
        """Récupère les statistiques des commandes"""
        try:
            today = datetime.now().date()
            
            # Total des commandes
            total_orders = self.order_repo.count()
            
            # Nouvelles commandes aujourd'hui
            new_today = self.order_repo.count_by_date(today)
            
            # Commandes en attente
            pending_orders = self.order_repo.count_by_status('en_attente')
            
            return {
                'total': total_orders,
                'new_today': new_today,
                'pending': pending_orders
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques commandes: {str(e)}")
    
    def get_revenue_stats(self) -> Dict[str, float]:
        """Récupère les statistiques du chiffre d'affaires"""
        try:
            today = datetime.now().date()
            start_of_month = today.replace(day=1)
            
            # CA total
            total_revenue = self.order_repo.get_total_revenue()
            
            # CA aujourd'hui
            today_revenue = self.order_repo.get_revenue_by_date(today)
            
            # CA ce mois
            month_revenue = self.order_repo.get_revenue_by_date_range(start_of_month, today)
            
            return {
                'total': total_revenue or 0.0,
                'today': today_revenue or 0.0,
                'this_month': month_revenue or 0.0
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques CA: {str(e)}")
    
    def get_orders_chart_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """Récupère les données pour le graphique des commandes"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            chart_data = self.order_repo.get_orders_by_date_range(start_date, end_date)
            
            return chart_data
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des données graphique commandes: {str(e)}")
    
    def get_revenue_chart_data(self, days: int = 30) -> List[Dict[str, Any]]:
        """Récupère les données pour le graphique du chiffre d'affaires"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            chart_data = self.order_repo.get_revenue_by_date_range_chart(start_date, end_date)
            
            return chart_data
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des données graphique CA: {str(e)}")
    
    def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupère les produits les plus vendus"""
        try:
            top_products = self.line_repo.get_top_products(limit)
            
            return top_products
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des top produits: {str(e)}")
    
    def get_orders_by_status(self) -> List[Dict[str, Any]]:
        """Récupère la répartition des commandes par statut"""
        try:
            orders_by_status = self.order_repo.get_orders_by_status()
            
            return orders_by_status
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des commandes par statut: {str(e)}")
    
    def get_daily_stats(self, date: datetime.date) -> Dict[str, Any]:
        """Récupère les statistiques d'une journée spécifique"""
        try:
            # Utilisateurs créés ce jour
            users_created = self.user_repo.count_by_date(date)
            
            # Produits créés ce jour
            products_created = self.product_repo.count_by_date(date)
            
            # Commandes créées ce jour
            orders_created = self.order_repo.count_by_date(date)
            
            # CA du jour
            daily_revenue = self.order_repo.get_revenue_by_date(date)
            
            return {
                'date': date.isoformat(),
                'users_created': users_created,
                'products_created': products_created,
                'orders_created': orders_created,
                'revenue': daily_revenue or 0.0
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques journalières: {str(e)}")
    
    def get_weekly_stats(self, week_start: datetime.date) -> Dict[str, Any]:
        """Récupère les statistiques d'une semaine"""
        try:
            week_end = week_start + timedelta(days=6)
            
            # Utilisateurs créés cette semaine
            users_created = self.user_repo.count_by_date_range(week_start, week_end)
            
            # Produits créés cette semaine
            products_created = self.product_repo.count_by_date_range(week_start, week_end)
            
            # Commandes créées cette semaine
            orders_created = self.order_repo.count_by_date_range(week_start, week_end)
            
            # CA de la semaine
            weekly_revenue = self.order_repo.get_revenue_by_date_range(week_start, week_end)
            
            return {
                'week_start': week_start.isoformat(),
                'week_end': week_end.isoformat(),
                'users_created': users_created,
                'products_created': products_created,
                'orders_created': orders_created,
                'revenue': weekly_revenue or 0.0
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques hebdomadaires: {str(e)}")
    
    def get_monthly_stats(self, month: int, year: int) -> Dict[str, Any]:
        """Récupère les statistiques d'un mois"""
        try:
            from datetime import date
            month_start = date(year, month, 1)
            
            # Calculer le dernier jour du mois
            if month == 12:
                month_end = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(year, month + 1, 1) - timedelta(days=1)
            
            # Utilisateurs créés ce mois
            users_created = self.user_repo.count_by_date_range(month_start, month_end)
            
            # Produits créés ce mois
            products_created = self.product_repo.count_by_date_range(month_start, month_end)
            
            # Commandes créées ce mois
            orders_created = self.order_repo.count_by_date_range(month_start, month_end)
            
            # CA du mois
            monthly_revenue = self.order_repo.get_revenue_by_date_range(month_start, month_end)
            
            return {
                'month': month,
                'year': year,
                'month_start': month_start.isoformat(),
                'month_end': month_end.isoformat(),
                'users_created': users_created,
                'products_created': products_created,
                'orders_created': orders_created,
                'revenue': monthly_revenue or 0.0
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des statistiques mensuelles: {str(e)}")
