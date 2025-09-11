"""
Contrôleur pour l'authentification
"""

import logging
from flask import request
from flask_restx import Resource, Namespace
from ...service.impl.auth_service import AuthService
from ..dto.auth_dto import register_model, login_model, token_response_model, error_model

# Configuration du logger
logger = logging.getLogger(__name__)

# Créer un namespace pour l'authentification
auth_ns = Namespace('auth', description='Opérations d\'authentification')

@auth_ns.route('/register')
class Register(Resource):
    """Endpoint pour l'inscription d'un nouvel utilisateur"""
    
    @auth_ns.expect(register_model)
    def post(self):
        """Inscrit un nouvel utilisateur"""
        logger.info("=== DÉBUT INSCRIPTION ===")
        try:
            data = request.get_json()
            logger.info(f"Données reçues: {data}")
            
            # Validation des données
            if not data:
                logger.warning("Aucune donnée JSON reçue")
                return {'message': 'Données JSON requises', 'error': 'validation_error'}, 400
            
            email = data.get('email')
            mot_de_passe = data.get('mot_de_passe')
            nom = data.get('nom')
            role = data.get('role', 'client')
            
            logger.info(f"Données extraites - Email: {email}, Nom: {nom}, Rôle: {role}, Mot de passe: {'***' if mot_de_passe else 'VIDE'}")
            
            if not all([email, mot_de_passe, nom]):
                logger.warning(f"Champs manquants - Email: {bool(email)}, Mot de passe: {bool(mot_de_passe)}, Nom: {bool(nom)}")
                return {'message': 'Email, mot de passe et nom sont requis', 'error': 'validation_error'}, 400
            
            # Validation de l'email
            if '@' not in email or '.' not in email:
                logger.warning(f"Format d'email invalide: {email}")
                return {'message': 'Format d\'email invalide', 'error': 'validation_error'}, 400
            
            # Validation du mot de passe
            if len(mot_de_passe) < 6:
                logger.warning(f"Mot de passe trop court: {len(mot_de_passe)} caractères")
                return {'message': 'Le mot de passe doit contenir au moins 6 caractères', 'error': 'validation_error'}, 400
            
            logger.info("Validation des données réussie, création de l'utilisateur...")
            
            # Créer l'utilisateur
            auth_service = AuthService()
            result = auth_service.register_user(email, mot_de_passe, nom, role)
            logger.info(f"Résultat de l'inscription: {result}")
            
            if not result or not result.get('success'):
                logger.error(f"Échec de l'inscription: {result}")
                return result, 400
            
            # Générer un token pour l'utilisateur nouvellement créé
            logger.info("Génération du token de connexion...")
            login_result = auth_service.login_user(email, mot_de_passe)
            logger.info(f"Résultat de la connexion: {login_result}")
            
            logger.info("=== INSCRIPTION RÉUSSIE ===")
            return login_result, 201
            
        except ValueError as e:
            logger.error(f"Erreur de validation: {str(e)}")
            return {'message': str(e), 'error': 'validation_error'}, 400
        except Exception as e:
            logger.error(f"Erreur interne lors de l'inscription: {str(e)}", exc_info=True)
            return {'message': 'Erreur interne du serveur', 'error': 'internal_error'}, 500

@auth_ns.route('/login')
class Login(Resource):
    """Endpoint pour la connexion d'un utilisateur"""
    
    @auth_ns.expect(login_model)
    def post(self):
        """Connecte un utilisateur et retourne un token JWT"""
        logger.info("=== DÉBUT CONNEXION ===")
        try:
            data = request.get_json()
            logger.info(f"Données de connexion reçues: {data}")
            
            # Validation des données
            if not data:
                logger.warning("Aucune donnée JSON reçue pour la connexion")
                return {'message': 'Données JSON requises', 'error': 'validation_error'}, 400
            
            email = data.get('email')
            mot_de_passe = data.get('mot_de_passe')
            
            logger.info(f"Données extraites - Email: {email}, Mot de passe: {'***' if mot_de_passe else 'VIDE'}")
            
            if not all([email, mot_de_passe]):
                logger.warning(f"Champs manquants pour la connexion - Email: {bool(email)}, Mot de passe: {bool(mot_de_passe)}")
                return {'message': 'Email et mot de passe sont requis', 'error': 'validation_error'}, 400
            
            logger.info("Validation des données réussie, authentification...")
            
            # Authentifier l'utilisateur
            auth_service = AuthService()
            result = auth_service.login_user(email, mot_de_passe)
            logger.info(f"Résultat de l'authentification: {result}")
            
            if not result or not result.get('success'):
                logger.warning(f"Échec de l'authentification pour {email}: {result}")
                return result, 401
            
            logger.info(f"=== CONNEXION RÉUSSIE pour {email} ===")
            return result, 200
            
        except ValueError as e:
            logger.error(f"Erreur de validation lors de la connexion: {str(e)}")
            return {'message': str(e), 'error': 'authentication_error'}, 401
        except Exception as e:
            logger.error(f"Erreur interne lors de la connexion: {str(e)}", exc_info=True)
            return {'message': 'Erreur interne du serveur', 'error': 'internal_error'}, 500

@auth_ns.route('/verify')
class VerifyToken(Resource):
    """Endpoint pour vérifier un token JWT"""
    
    @auth_ns.marshal_with(error_model, code=401)
    def get(self):
        """Vérifie la validité d'un token JWT"""
        try:
            # Récupérer le token depuis l'en-tête Authorization
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {'message': 'Token d\'authentification requis', 'error': 'missing_token'}, 401
            
            # Extraire le token (format: "Bearer <token>")
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return {'message': 'Format de token invalide', 'error': 'invalid_token_format'}, 401
            
            # Vérifier le token
            auth_service = AuthService()
            token_data = auth_service.verify_token(token)
            
            if not token_data:
                return {'message': 'Token invalide ou expiré', 'error': 'invalid_token'}, 401
            
            return {
                'valid': True,
                'user': token_data['user']
            }, 200
            
        except Exception as e:
            return {'message': 'Erreur interne du serveur', 'error': 'internal_error'}, 500

@auth_ns.route('/refresh')
class RefreshToken(Resource):
    """Endpoint pour rafraîchir un token JWT"""
    
    @auth_ns.marshal_with(token_response_model, code=200)
    @auth_ns.marshal_with(error_model, code=401)
    def post(self):
        """Rafraîchit un token JWT"""
        try:
            # Récupérer le token depuis l'en-tête Authorization
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return {'message': 'Token d\'authentification requis', 'error': 'missing_token'}, 401
            
            # Extraire le token
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return {'message': 'Format de token invalide', 'error': 'invalid_token_format'}, 401
            
            # Rafraîchir le token
            auth_service = AuthService()
            result = auth_service.refresh_token(token)
            
            if not result:
                return {'message': 'Token invalide ou expiré', 'error': 'invalid_token'}, 401
            
            return result, 200
            
        except Exception as e:
            return {'message': 'Erreur interne du serveur', 'error': 'internal_error'}, 500

