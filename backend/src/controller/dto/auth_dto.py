"""
DTOs pour l'authentification
"""

from flask_restx import fields
from ..api import api

# Modèles pour l'API Swagger
register_model = api.model('Register', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'mot_de_passe': fields.String(required=True, description='Mot de passe'),
    'nom': fields.String(required=True, description='Nom de l\'utilisateur'),
    'role': fields.String(required=False, description='Rôle (client ou admin)', default='client')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'mot_de_passe': fields.String(required=True, description='Mot de passe')
})

token_response_model = api.model('TokenResponse', {
    'access_token': fields.String(description='Token JWT'),
    'token_type': fields.String(description='Type de token', default='Bearer'),
    'expires_in': fields.Integer(description='Durée de validité en secondes'),
    'user': fields.Nested(api.model('UserInfo', {
        'id': fields.Integer(description='ID de l\'utilisateur'),
        'email': fields.String(description='Email'),
        'nom': fields.String(description='Nom'),
        'role': fields.String(description='Rôle')
    }))
})

error_model = api.model('Error', {
    'message': fields.String(description='Message d\'erreur'),
    'error': fields.String(description='Type d\'erreur')
})

