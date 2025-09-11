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
    prefix=''
)

# Import des namespaces
from .utilisateur_controller import utilisateur_ns
from .produit_controller import produit_ns
from .commande_controller import commande_ns
from .auth_controller import auth_ns

# Ajout des namespaces à l'API
api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(utilisateur_ns, path='/api/utilisateurs')
api.add_namespace(produit_ns, path='/api/produits')
api.add_namespace(commande_ns, path='/api/commandes')