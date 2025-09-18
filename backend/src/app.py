"""
Application principale avec architecture en couches
"""

import logging
from flask import Flask
from flask_migrate import Migrate
from .config.app_config import config
from .data.database.db import db
from .domain.models import Utilisateur, Produit, Commande, LigneCommande, Panier, PanierItem
from .utils.logging_config import configure_external_loggers, get_logger

# Configuration du logging
configure_external_loggers()
logger = get_logger(__name__)


def create_app(config_name='default'):
    """Factory pour créer l'application Flask"""
    
    logger.info(f"🚀 Création de l'application Flask avec config: {config_name}")
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    logger.info("✅ Configuration de l'application chargée")
    
    # Initialisation des extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Enregistrement des blueprints
    from .controller.api import api_bp
    app.register_blueprint(api_bp)
    
    # Route racine
    @app.route('/')
    def index():
        return {
            'message': 'API E-commerce avec Architecture en Couches',
            'version': '2.0.0',
            'architecture': 'Layered Architecture',
            'layers': {
                'domain': 'Entités métier et modèles',
                'data': 'Repositories et accès aux données',
                'service': 'Logique métier',
                'controller': 'Présentation et API'
            },
            'endpoints': {
                'auth': {
                    'register': '/api/auth/register',
                    'login': '/api/auth/login',
                    'verify': '/api/auth/verify',
                    'refresh': '/api/auth/refresh'
                },
                'utilisateurs': '/api/utilisateurs',
                'produits': '/api/produits',
                'commandes': '/api/commandes',
                'lignes_commande': '/api/lignes-commande',
                'statistiques': {
                    'general': '/api/stats/',
                    'utilisateurs': '/api/stats/users',
                    'produits': '/api/stats/products',
                    'commandes': '/api/stats/orders',
                    'chiffre_affaires': '/api/stats/revenue',
                    'graphiques': {
                        'commandes': '/api/stats/charts/orders',
                        'ca': '/api/stats/charts/revenue'
                    },
                    'top_produits': '/api/stats/top-products',
                    'commandes_par_statut': '/api/stats/orders-by-status'
                },
                'configuration': {
                    'general': '/api/config/',
                    'application': '/api/config/app',
                    'base_donnees': '/api/config/database',
                    'api': '/api/config/api',
                    'securite': '/api/config/security',
                    'reset': '/api/config/reset',
                    'backup': '/api/config/backup'
                },
                'maintenance': {
                    'optimiser_db': '/api/maintenance/optimize-db',
                    'nettoyer': '/api/maintenance/cleanup',
                    'performances': '/api/maintenance/performance',
                    'redemarrer_api': '/api/maintenance/restart',
                    'redemarrer_cache': '/api/maintenance/restart-cache',
                    'logs': '/api/maintenance/logs',
                    'sante': '/api/maintenance/health',
                    'statut': '/api/maintenance/status',
                    'sauvegarde': '/api/maintenance/backup',
                    'restauration': '/api/maintenance/restore'
                },
                'rapports': {
                    'generer': '/api/reports/generate',
                    'ventes': '/api/reports/sales',
                    'top_clients': '/api/reports/top-clients',
                    'top_produits': '/api/reports/top-products',
                    'analyse_commandes': '/api/reports/orders-analysis',
                    'performance': '/api/reports/performance',
                    'exporter': '/api/reports/export',
                    'programmes': '/api/reports/scheduled'
                }
            }
        }
    
    return app


def init_db(app):
    """Initialise la base de données"""
    with app.app_context():
        db.create_all()
        print("Base de données créée avec succès!")
        
        # Vérifier si la base est vide
        if Utilisateur.query.count() == 0:
            print("Base de données vide. Exécutez le script de données de test.")
