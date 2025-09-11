"""
Application principale avec architecture en couches
"""

import logging
from flask import Flask
from flask_migrate import Migrate
from .config.app_config import config
from .data.database.db import db
from .domain.models import Utilisateur, Produit, Commande, LigneCommande


def create_app(config_name='default'):
    """Factory pour créer l'application Flask"""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
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
                'lignes_commande': '/api/lignes-commande'
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
