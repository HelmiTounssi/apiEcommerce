"""
Contrôleur pour la maintenance
"""

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from ...utils.auth_decorators import token_required, admin_required
from ...service.impl.maintenance_service import MaintenanceService

# Créer le namespace pour la maintenance
maintenance_ns = Namespace('maintenance', description='Maintenance du système')

# Modèles de données pour la documentation Swagger
performance_model = maintenance_ns.model('Performance', {
    'avg_response_time': fields.Float(description='Temps de réponse moyen en ms'),
    'requests_per_minute': fields.Integer(description='Requêtes par minute'),
    'error_rate': fields.Float(description='Taux d\'erreur en %'),
    'memory_usage': fields.Float(description='Utilisation mémoire en MB'),
    'cpu_usage': fields.Float(description='Utilisation CPU en %'),
    'disk_usage': fields.Float(description='Utilisation disque en %')
})

@maintenance_ns.route('/optimize-db')
class OptimizeDatabaseResource(Resource):
    """Ressource pour optimiser la base de données"""
    
    @maintenance_ns.doc('optimize_database')
    @admin_required
    def post(self):
        """Optimise la base de données"""
        try:
            maintenance_service = MaintenanceService()
            result = maintenance_service.optimize_database()
            
            return {
                'success': True,
                'message': 'Base de données optimisée avec succès',
                'data': result
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de l\'optimisation: {str(e)}'
            }, 500

@maintenance_ns.route('/cleanup')
class CleanupResource(Resource):
    """Ressource pour nettoyer les données temporaires"""
    
    @maintenance_ns.doc('cleanup_temp_data')
    @admin_required
    def post(self):
        """Nettoie les données temporaires"""
        try:
            maintenance_service = MaintenanceService()
            result = maintenance_service.cleanup_temp_data()
            
            return {
                'success': True,
                'message': 'Données temporaires nettoyées avec succès',
                'data': result
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors du nettoyage: {str(e)}'
            }, 500

@maintenance_ns.route('/performance')
class PerformanceResource(Resource):
    """Ressource pour analyser les performances"""
    
    @maintenance_ns.doc('analyze_performance')
    @maintenance_ns.marshal_with(performance_model)
    @token_required
    def get(self):
        """Analyse les performances du système"""
        try:
            maintenance_service = MaintenanceService()
            performance_data = maintenance_service.analyze_performance()
            
            return {
                'success': True,
                'data': performance_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de l\'analyse des performances: {str(e)}'
            }, 500

@maintenance_ns.route('/restart')
class RestartApiResource(Resource):
    """Ressource pour redémarrer l'API"""
    
    @maintenance_ns.doc('restart_api')
    @admin_required
    def post(self):
        """Redémarre l'API"""
        try:
            maintenance_service = MaintenanceService()
            result = maintenance_service.restart_api()
            
            return {
                'success': True,
                'message': 'API redémarrée avec succès',
                'data': result
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors du redémarrage: {str(e)}'
            }, 500

@maintenance_ns.route('/restart-cache')
class RestartCacheResource(Resource):
    """Ressource pour redémarrer le cache"""
    
    @maintenance_ns.doc('restart_cache')
    @admin_required
    def post(self):
        """Redémarre le cache"""
        try:
            maintenance_service = MaintenanceService()
            result = maintenance_service.restart_cache()
            
            return {
                'success': True,
                'message': 'Cache redémarré avec succès',
                'data': result
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors du redémarrage du cache: {str(e)}'
            }, 500

@maintenance_ns.route('/logs')
class LogsResource(Resource):
    """Ressource pour récupérer les logs"""
    
    @maintenance_ns.doc('get_system_logs')
    @token_required
    def get(self):
        """Récupère les logs système"""
        try:
            level = request.args.get('level', 'INFO')
            lines = request.args.get('lines', 100, type=int)
            
            maintenance_service = MaintenanceService()
            logs = maintenance_service.get_system_logs(level, lines)
            
            return {
                'success': True,
                'data': logs
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des logs: {str(e)}'
            }, 500

@maintenance_ns.route('/health')
class HealthCheckResource(Resource):
    """Ressource pour vérifier la santé du système"""
    
    @maintenance_ns.doc('health_check')
    def get(self):
        """Vérifie la santé du système"""
        try:
            maintenance_service = MaintenanceService()
            health_data = maintenance_service.health_check()
            
            return {
                'success': True,
                'data': health_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la vérification de santé: {str(e)}'
            }, 500

@maintenance_ns.route('/status')
class SystemStatusResource(Resource):
    """Ressource pour le statut du système"""
    
    @maintenance_ns.doc('get_system_status')
    @token_required
    def get(self):
        """Récupère le statut du système"""
        try:
            maintenance_service = MaintenanceService()
            status_data = maintenance_service.get_system_status()
            
            return {
                'success': True,
                'data': status_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération du statut: {str(e)}'
            }, 500

@maintenance_ns.route('/backup')
class BackupResource(Resource):
    """Ressource pour sauvegarder le système"""
    
    @maintenance_ns.doc('backup_system')
    @admin_required
    def post(self):
        """Sauvegarde le système"""
        try:
            backup_type = request.args.get('type', 'full')
            maintenance_service = MaintenanceService()
            backup_result = maintenance_service.backup_system(backup_type)
            
            return {
                'success': True,
                'message': 'Sauvegarde effectuée avec succès',
                'data': backup_result
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la sauvegarde: {str(e)}'
            }, 500

@maintenance_ns.route('/restore')
class RestoreResource(Resource):
    """Ressource pour restaurer le système"""
    
    @maintenance_ns.doc('restore_system')
    @admin_required
    def post(self):
        """Restaure le système"""
        try:
            backup_file = request.args.get('backup_file')
            if not backup_file:
                return {
                    'success': False,
                    'message': 'Fichier de sauvegarde manquant'
                }, 400
            
            maintenance_service = MaintenanceService()
            restore_result = maintenance_service.restore_system(backup_file)
            
            return {
                'success': True,
                'message': 'Restauration effectuée avec succès',
                'data': restore_result
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la restauration: {str(e)}'
            }, 500
