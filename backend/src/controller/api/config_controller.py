"""
Contrôleur pour la configuration
"""

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from ...utils.auth_decorators import token_required, admin_required
from ...service.impl.config_service import ConfigService

# Créer le namespace pour la configuration
config_ns = Namespace('config', description='Configuration du système')

# Modèles de données pour la documentation Swagger
config_model = config_ns.model('Config', {
    'app_name': fields.String(description='Nom de l\'application'),
    'debug_mode': fields.Boolean(description='Mode debug'),
    'maintenance_mode': fields.Boolean(description='Mode maintenance'),
    'database': fields.Nested(config_ns.model('DatabaseConfig', {
        'type': fields.String(description='Type de base de données'),
        'pool_size': fields.Integer(description='Taille du pool de connexions')
    })),
    'api': fields.Nested(config_ns.model('ApiConfig', {
        'timeout': fields.Integer(description='Timeout API en secondes'),
        'max_requests_per_minute': fields.Integer(description='Max requêtes par minute')
    })),
    'security': fields.Nested(config_ns.model('SecurityConfig', {
        'jwt_expiration': fields.Integer(description='Expiration JWT en heures'),
        'password_min_length': fields.Integer(description='Longueur minimale du mot de passe')
    }))
})

@config_ns.route('/')
class ConfigResource(Resource):
    """Ressource pour la configuration"""
    
    @config_ns.doc('get_config')
    @config_ns.marshal_with(config_model)
    @token_required
    def get(self):
        """Récupère la configuration actuelle"""
        try:
            config_service = ConfigService()
            config = config_service.get_current_config()
            
            return {
                'success': True,
                'data': config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération de la configuration: {str(e)}'
            }, 500
    
    @config_ns.doc('update_config')
    @config_ns.expect(config_model)
    @admin_required
    def post(self):
        """Met à jour la configuration"""
        try:
            config_data = request.get_json()
            
            if not config_data:
                return {
                    'success': False,
                    'message': 'Données de configuration manquantes'
                }, 400
            
            config_service = ConfigService()
            updated_config = config_service.update_config(config_data)
            
            return {
                'success': True,
                'message': 'Configuration mise à jour avec succès',
                'data': updated_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la mise à jour de la configuration: {str(e)}'
            }, 500

@config_ns.route('/app')
class AppConfigResource(Resource):
    """Ressource pour la configuration de l'application"""
    
    @config_ns.doc('get_app_config')
    @token_required
    def get(self):
        """Récupère la configuration de l'application"""
        try:
            config_service = ConfigService()
            app_config = config_service.get_app_config()
            
            return {
                'success': True,
                'data': app_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération de la config app: {str(e)}'
            }, 500
    
    @config_ns.doc('update_app_config')
    @admin_required
    def post(self):
        """Met à jour la configuration de l'application"""
        try:
            app_data = request.get_json()
            
            if not app_data:
                return {
                    'success': False,
                    'message': 'Données de configuration app manquantes'
                }, 400
            
            config_service = ConfigService()
            updated_config = config_service.update_app_config(app_data)
            
            return {
                'success': True,
                'message': 'Configuration app mise à jour avec succès',
                'data': updated_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la mise à jour de la config app: {str(e)}'
            }, 500

@config_ns.route('/database')
class DatabaseConfigResource(Resource):
    """Ressource pour la configuration de la base de données"""
    
    @config_ns.doc('get_database_config')
    @token_required
    def get(self):
        """Récupère la configuration de la base de données"""
        try:
            config_service = ConfigService()
            db_config = config_service.get_database_config()
            
            return {
                'success': True,
                'data': db_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération de la config DB: {str(e)}'
            }, 500
    
    @config_ns.doc('update_database_config')
    @admin_required
    def post(self):
        """Met à jour la configuration de la base de données"""
        try:
            db_data = request.get_json()
            
            if not db_data:
                return {
                    'success': False,
                    'message': 'Données de configuration DB manquantes'
                }, 400
            
            config_service = ConfigService()
            updated_config = config_service.update_database_config(db_data)
            
            return {
                'success': True,
                'message': 'Configuration DB mise à jour avec succès',
                'data': updated_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la mise à jour de la config DB: {str(e)}'
            }, 500

@config_ns.route('/api')
class ApiConfigResource(Resource):
    """Ressource pour la configuration de l'API"""
    
    @config_ns.doc('get_api_config')
    @token_required
    def get(self):
        """Récupère la configuration de l'API"""
        try:
            config_service = ConfigService()
            api_config = config_service.get_api_config()
            
            return {
                'success': True,
                'data': api_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération de la config API: {str(e)}'
            }, 500
    
    @config_ns.doc('update_api_config')
    @admin_required
    def post(self):
        """Met à jour la configuration de l'API"""
        try:
            api_data = request.get_json()
            
            if not api_data:
                return {
                    'success': False,
                    'message': 'Données de configuration API manquantes'
                }, 400
            
            config_service = ConfigService()
            updated_config = config_service.update_api_config(api_data)
            
            return {
                'success': True,
                'message': 'Configuration API mise à jour avec succès',
                'data': updated_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la mise à jour de la config API: {str(e)}'
            }, 500

@config_ns.route('/security')
class SecurityConfigResource(Resource):
    """Ressource pour la configuration de sécurité"""
    
    @config_ns.doc('get_security_config')
    @token_required
    def get(self):
        """Récupère la configuration de sécurité"""
        try:
            config_service = ConfigService()
            security_config = config_service.get_security_config()
            
            return {
                'success': True,
                'data': security_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération de la config sécurité: {str(e)}'
            }, 500
    
    @config_ns.doc('update_security_config')
    @admin_required
    def post(self):
        """Met à jour la configuration de sécurité"""
        try:
            security_data = request.get_json()
            
            if not security_data:
                return {
                    'success': False,
                    'message': 'Données de configuration sécurité manquantes'
                }, 400
            
            config_service = ConfigService()
            updated_config = config_service.update_security_config(security_data)
            
            return {
                'success': True,
                'message': 'Configuration sécurité mise à jour avec succès',
                'data': updated_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la mise à jour de la config sécurité: {str(e)}'
            }, 500

@config_ns.route('/reset')
class ResetConfigResource(Resource):
    """Ressource pour réinitialiser la configuration"""
    
    @config_ns.doc('reset_config')
    @admin_required
    def post(self):
        """Réinitialise la configuration aux valeurs par défaut"""
        try:
            config_service = ConfigService()
            default_config = config_service.reset_to_default()
            
            return {
                'success': True,
                'message': 'Configuration réinitialisée aux valeurs par défaut',
                'data': default_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la réinitialisation: {str(e)}'
            }, 500

@config_ns.route('/backup')
class BackupConfigResource(Resource):
    """Ressource pour sauvegarder/restaurer la configuration"""
    
    @config_ns.doc('backup_config')
    @admin_required
    def post(self):
        """Sauvegarde la configuration actuelle"""
        try:
            config_service = ConfigService()
            backup_data = config_service.backup_config()
            
            return {
                'success': True,
                'message': 'Configuration sauvegardée avec succès',
                'data': backup_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la sauvegarde: {str(e)}'
            }, 500
    
    @config_ns.doc('restore_config')
    @admin_required
    def put(self):
        """Restaure une configuration sauvegardée"""
        try:
            backup_data = request.get_json()
            
            if not backup_data:
                return {
                    'success': False,
                    'message': 'Données de sauvegarde manquantes'
                }, 400
            
            config_service = ConfigService()
            restored_config = config_service.restore_config(backup_data)
            
            return {
                'success': True,
                'message': 'Configuration restaurée avec succès',
                'data': restored_config
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la restauration: {str(e)}'
            }, 500
