"""
Service d'authentification
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from flask import current_app
from ...data.repositories.utilisateur_repository import UtilisateurRepository
from ...domain.models.utilisateur import Utilisateur

# Configuration du logger
logger = logging.getLogger(__name__)


class AuthService:
    """Service pour la gestion de l'authentification"""
    
    def __init__(self):
        self.utilisateur_repo = UtilisateurRepository()
        self.secret_key = current_app.config.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
        self.jwt_expiration = current_app.config.get('JWT_EXPIRATION', 3600)  # 1 heure par défaut
    
    def register_user(self, email: str, mot_de_passe: str, nom: str, role: str = 'client') -> Dict[str, Any]:
        """
        Inscrit un nouvel utilisateur
        
        Args:
            email: Email de l'utilisateur
            mot_de_passe: Mot de passe en clair
            nom: Nom de l'utilisateur
            role: Rôle de l'utilisateur (client ou admin)
            
        Returns:
            Dict contenant les informations de l'utilisateur créé
            
        Raises:
            ValueError: Si l'email existe déjà ou si les données sont invalides
        """
        logger.info(f"Tentative d'inscription pour l'email: {email}")
        
        # Vérifier si l'email existe déjà
        existing_user = self.utilisateur_repo.get_by_email(email)
        if existing_user:
            logger.warning(f"Email déjà utilisé: {email}")
            raise ValueError("Un utilisateur avec cet email existe déjà")
        
        logger.info(f"Email {email} disponible, validation du rôle: {role}")
        
        # Valider le rôle
        if role not in ['client', 'admin']:
            logger.error(f"Rôle invalide: {role}")
            raise ValueError("Le rôle doit être 'client' ou 'admin'")
        
        logger.info(f"Création de l'utilisateur: {email}, {nom}, {role}")
        
        # Créer l'utilisateur
        try:
            utilisateur = self.utilisateur_repo.create_user(
                email=email,
                mot_de_passe=mot_de_passe,
                nom=nom,
                role=role
            )
            logger.info(f"Utilisateur créé avec succès - ID: {utilisateur.id}")
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'utilisateur: {str(e)}")
            raise
        
        return {
            'success': True,
            'message': 'Utilisateur créé avec succès',
            'user': utilisateur.to_dict()
        }
    
    def login_user(self, email: str, mot_de_passe: str) -> Dict[str, Any]:
        """
        Connecte un utilisateur et génère un token JWT
        
        Args:
            email: Email de l'utilisateur
            mot_de_passe: Mot de passe en clair
            
        Returns:
            Dict contenant le token JWT et les informations utilisateur
            
        Raises:
            ValueError: Si les identifiants sont incorrects
        """
        logger.info(f"Tentative de connexion pour l'email: {email}")
        
        # Récupérer l'utilisateur par email
        utilisateur = self.utilisateur_repo.get_by_email(email)
        if not utilisateur:
            logger.warning(f"Utilisateur non trouvé pour l'email: {email}")
            raise ValueError("Email ou mot de passe incorrect")
        
        logger.info(f"Utilisateur trouvé - ID: {utilisateur.id}, Email: {utilisateur.email}")
        
        # Vérifier le mot de passe
        if not utilisateur.check_password(mot_de_passe):
            logger.warning(f"Mot de passe incorrect pour l'utilisateur: {email}")
            raise ValueError("Email ou mot de passe incorrect")
        
        logger.info(f"Authentification réussie pour: {email}")
        
        # Générer le token JWT
        token = self._generate_jwt_token(utilisateur)
        logger.info(f"Token JWT généré pour: {email}")
        
        return {
            'success': True,
            'token': token,
            'access_token': token,  # Pour compatibilité
            'token_type': 'Bearer',
            'expires_in': self.jwt_expiration,
            'utilisateur': utilisateur.to_dict()
        }
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Vérifie et décode un token JWT
        
        Args:
            token: Token JWT à vérifier
            
        Returns:
            Dict contenant les informations de l'utilisateur ou None si invalide
        """
        try:
            # Décoder le token
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            # Récupérer l'utilisateur
            user_id = payload.get('user_id')
            if not user_id:
                return None
            
            utilisateur = self.utilisateur_repo.get_by_id(user_id)
            if not utilisateur:
                return None
            
            return {
                'user_id': user_id,
                'email': payload.get('email'),
                'role': payload.get('role'),
                'user': utilisateur.to_dict()
            }
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def get_user_by_token(self, token: str) -> Optional[Utilisateur]:
        """
        Récupère un utilisateur à partir de son token JWT
        
        Args:
            token: Token JWT
            
        Returns:
            Utilisateur ou None si le token est invalide
        """
        token_data = self.verify_token(token)
        if not token_data:
            return None
        
        return self.utilisateur_repo.get_by_id(token_data['user_id'])
    
    def _generate_jwt_token(self, utilisateur: Utilisateur) -> str:
        """
        Génère un token JWT pour un utilisateur
        
        Args:
            utilisateur: Utilisateur pour lequel générer le token
            
        Returns:
            Token JWT encodé
        """
        # Payload du token
        payload = {
            'user_id': utilisateur.id,
            'email': utilisateur.email,
            'role': utilisateur.role,
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_expiration),
            'iat': datetime.utcnow()
        }
        
        # Encoder le token
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def refresh_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Rafraîchit un token JWT
        
        Args:
            token: Token JWT actuel
            
        Returns:
            Nouveau token ou None si le token actuel est invalide
        """
        token_data = self.verify_token(token)
        if not token_data:
            return None
        
        utilisateur = self.utilisateur_repo.get_by_id(token_data['user_id'])
        if not utilisateur:
            return None
        
        # Générer un nouveau token
        new_token = self._generate_jwt_token(utilisateur)
        
        return {
            'access_token': new_token,
            'token_type': 'Bearer',
            'expires_in': self.jwt_expiration,
            'user': utilisateur.to_dict()
        }

