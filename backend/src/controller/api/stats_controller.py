"""
Contrôleur pour les statistiques
"""

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from ...utils.auth_decorators import token_required, admin_required
from ...service.impl.stats_service import StatsService

# Créer le namespace pour les statistiques
stats_ns = Namespace('stats', description='Statistiques du système')

# Modèles de données pour la documentation Swagger
stats_model = stats_ns.model('Stats', {
    'users': fields.Nested(stats_ns.model('UserStats', {
        'total': fields.Integer(description='Nombre total d\'utilisateurs'),
        'new_today': fields.Integer(description='Nouveaux utilisateurs aujourd\'hui'),
        'active': fields.Integer(description='Utilisateurs actifs')
    })),
    'products': fields.Nested(stats_ns.model('ProductStats', {
        'total': fields.Integer(description='Nombre total de produits'),
        'new_today': fields.Integer(description='Nouveaux produits aujourd\'hui'),
        'low_stock': fields.Integer(description='Produits en rupture de stock')
    })),
    'orders': fields.Nested(stats_ns.model('OrderStats', {
        'total': fields.Integer(description='Nombre total de commandes'),
        'new_today': fields.Integer(description='Nouvelles commandes aujourd\'hui'),
        'pending': fields.Integer(description='Commandes en attente')
    })),
    'revenue': fields.Nested(stats_ns.model('RevenueStats', {
        'total': fields.Float(description='Chiffre d\'affaires total'),
        'today': fields.Float(description='Chiffre d\'affaires aujourd\'hui'),
        'this_month': fields.Float(description='Chiffre d\'affaires ce mois')
    }))
})

@stats_ns.route('/')
class StatsResource(Resource):
    """Ressource pour les statistiques générales"""
    
    @stats_ns.doc('get_stats')
    @stats_ns.marshal_with(stats_model)
    @token_required
    def get(self):
        """Récupère les statistiques générales du système"""
        try:
            stats_service = StatsService()
            stats = stats_service.get_general_stats()
            
            return {
                'success': True,
                'data': stats
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des statistiques: {str(e)}'
            }, 500

@stats_ns.route('/users')
class UserStatsResource(Resource):
    """Ressource pour les statistiques des utilisateurs"""
    
    @stats_ns.doc('get_user_stats')
    @token_required
    def get(self):
        """Récupère les statistiques des utilisateurs"""
        try:
            stats_service = StatsService()
            user_stats = stats_service.get_user_stats()
            
            return {
                'success': True,
                'data': user_stats
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des statistiques utilisateurs: {str(e)}'
            }, 500

@stats_ns.route('/products')
class ProductStatsResource(Resource):
    """Ressource pour les statistiques des produits"""
    
    @stats_ns.doc('get_product_stats')
    @token_required
    def get(self):
        """Récupère les statistiques des produits"""
        try:
            stats_service = StatsService()
            product_stats = stats_service.get_product_stats()
            
            return {
                'success': True,
                'data': product_stats
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des statistiques produits: {str(e)}'
            }, 500

@stats_ns.route('/orders')
class OrderStatsResource(Resource):
    """Ressource pour les statistiques des commandes"""
    
    @stats_ns.doc('get_order_stats')
    @token_required
    def get(self):
        """Récupère les statistiques des commandes"""
        try:
            stats_service = StatsService()
            order_stats = stats_service.get_order_stats()
            
            return {
                'success': True,
                'data': order_stats
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des statistiques commandes: {str(e)}'
            }, 500

@stats_ns.route('/revenue')
class RevenueStatsResource(Resource):
    """Ressource pour les statistiques de chiffre d'affaires"""
    
    @stats_ns.doc('get_revenue_stats')
    @token_required
    def get(self):
        """Récupère les statistiques de chiffre d'affaires"""
        try:
            stats_service = StatsService()
            revenue_stats = stats_service.get_revenue_stats()
            
            return {
                'success': True,
                'data': revenue_stats
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des statistiques CA: {str(e)}'
            }, 500

@stats_ns.route('/charts/orders')
class OrderChartResource(Resource):
    """Ressource pour les données de graphique des commandes"""
    
    @stats_ns.doc('get_order_chart_data')
    @token_required
    def get(self):
        """Récupère les données pour le graphique des commandes"""
        try:
            days = request.args.get('days', 30, type=int)
            stats_service = StatsService()
            chart_data = stats_service.get_orders_chart_data(days)
            
            return {
                'success': True,
                'data': chart_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des données graphique: {str(e)}'
            }, 500

@stats_ns.route('/charts/revenue')
class RevenueChartResource(Resource):
    """Ressource pour les données de graphique du chiffre d'affaires"""
    
    @stats_ns.doc('get_revenue_chart_data')
    @token_required
    def get(self):
        """Récupère les données pour le graphique du chiffre d'affaires"""
        try:
            days = request.args.get('days', 30, type=int)
            stats_service = StatsService()
            chart_data = stats_service.get_revenue_chart_data(days)
            
            return {
                'success': True,
                'data': chart_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des données graphique CA: {str(e)}'
            }, 500

@stats_ns.route('/top-products')
class TopProductsResource(Resource):
    """Ressource pour les produits les plus vendus"""
    
    @stats_ns.doc('get_top_products')
    @token_required
    def get(self):
        """Récupère les produits les plus vendus"""
        try:
            limit = request.args.get('limit', 10, type=int)
            stats_service = StatsService()
            top_products = stats_service.get_top_products(limit)
            
            return {
                'success': True,
                'data': top_products
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des top produits: {str(e)}'
            }, 500

@stats_ns.route('/orders-by-status')
class OrdersByStatusResource(Resource):
    """Ressource pour les commandes par statut"""
    
    @stats_ns.doc('get_orders_by_status')
    @token_required
    def get(self):
        """Récupère la répartition des commandes par statut"""
        try:
            stats_service = StatsService()
            orders_by_status = stats_service.get_orders_by_status()
            
            return {
                'success': True,
                'data': orders_by_status
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des commandes par statut: {str(e)}'
            }, 500
