"""
API REST avec architecture en couches
"""

from flask import Blueprint
from flask_restx import Api, fields

# Création du blueprint API
api_bp = Blueprint('api', __name__)

# Configuration de l'API RESTX
api = Api(
    api_bp,
    version='2.0',
    title='API E-commerce - Architecture en Couches',
    description='API REST pour une application e-commerce avec architecture en couches',
    doc='/docs/',
    prefix='/api'
)

# Import des namespaces
from .utilisateur_controller import utilisateur_ns
from .produit_controller import produit_ns
from .commande_controller import commande_ns
from .auth_controller import auth_ns
from .panier_controller import panier_ns
from .stats_controller import stats_ns
from .config_controller import config_ns
from .maintenance_controller import maintenance_ns
from .reports_controller import reports_ns

# Ajout des namespaces à l'API
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(utilisateur_ns, path='/utilisateurs')
api.add_namespace(produit_ns, path='/produits')
api.add_namespace(commande_ns, path='/commandes')
api.add_namespace(panier_ns, path='/panier')
api.add_namespace(stats_ns, path='/stats')
api.add_namespace(config_ns, path='/config')
api.add_namespace(maintenance_ns, path='/maintenance')
api.add_namespace(reports_ns, path='/reports')