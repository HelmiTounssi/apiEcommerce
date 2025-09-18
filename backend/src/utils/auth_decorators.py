"""
Décorateurs pour l'authentification et l'autorisation
"""

from functools import wraps
from flask import request, jsonify
from ..service.impl.auth_service import AuthService


def token_required(f):
    """
    Décorateur pour protéger une route avec un token JWT
    
    Usage:
        @token_required
        def protected_route():
            # current_user est disponible dans g.current_user
            pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Récupérer le token depuis l'en-tête Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token d\'authentification requis', 'error': 'missing_token'}), 401
        
        # Extraire le token (format: "Bearer <token>")
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'message': 'Format de token invalide', 'error': 'invalid_token_format'}), 401
        
        # Vérifier le token
        auth_service = AuthService()
        token_data = auth_service.verify_token(token)
        
        if not token_data:
            return jsonify({'message': 'Token invalide ou expiré', 'error': 'invalid_token'}), 401
        
        # Ajouter les informations utilisateur à la requête
        from flask import g
        g.current_user = token_data['user']
        g.current_user_id = token_data['user_id']
        g.current_user_role = token_data['role']
        
        return f(*args, **kwargs)
    
    return decorated


def admin_required(f):
    """
    Décorateur pour protéger une route avec un token JWT et vérifier le rôle admin
    
    Usage:
        @admin_required
        def admin_route():
            # current_user est disponible dans g.current_user
            pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Récupérer le token depuis l'en-tête Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token d\'authentification requis', 'error': 'missing_token'}), 401
        
        # Extraire le token
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'message': 'Format de token invalide', 'error': 'invalid_token_format'}), 401
        
        # Vérifier le token
        auth_service = AuthService()
        token_data = auth_service.verify_token(token)
        
        if not token_data:
            return jsonify({'message': 'Token invalide ou expiré', 'error': 'invalid_token'}), 401
        
        # Vérifier le rôle admin
        if token_data['role'] != 'admin':
            return jsonify({'message': 'Accès refusé. Rôle administrateur requis', 'error': 'insufficient_permissions'}), 403
        
        # Ajouter les informations utilisateur à la requête
        from flask import g
        g.current_user = token_data['user']
        g.current_user_id = token_data['user_id']
        g.current_user_role = token_data['role']
        
        return f(*args, **kwargs)
    
    return decorated


def client_or_admin_required(f):
    """
    Décorateur pour protéger une route avec un token JWT (client ou admin)
    
    Usage:
        @client_or_admin_required
        def protected_route():
            # current_user est disponible dans g.current_user
            pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Récupérer le token depuis l'en-tête Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token d\'authentification requis', 'error': 'missing_token'}), 401
        
        # Extraire le token
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'message': 'Format de token invalide', 'error': 'invalid_token_format'}), 401
        
        # Vérifier le token
        auth_service = AuthService()
        token_data = auth_service.verify_token(token)
        
        if not token_data:
            return jsonify({'message': 'Token invalide ou expiré', 'error': 'invalid_token'}), 401
        
        # Vérifier le rôle (client ou admin)
        if token_data['role'] not in ['client', 'admin']:
            return jsonify({'message': 'Accès refusé. Rôle client ou administrateur requis', 'error': 'insufficient_permissions'}), 403
        
        # Ajouter les informations utilisateur à la requête
        from flask import g
        g.current_user = token_data['user']
        g.current_user_id = token_data['user_id']
        g.current_user_role = token_data['role']
        
        return f(*args, **kwargs)
    
    return decorated


def get_current_user():
    """
    Récupère l'utilisateur actuel depuis le contexte Flask
    
    Returns:
        Dict contenant les informations de l'utilisateur ou None
    """
    from flask import g
    return getattr(g, 'current_user', None)


def get_current_user_id():
    """
    Récupère l'ID de l'utilisateur actuel depuis le contexte Flask
    
    Returns:
        ID de l'utilisateur ou None
    """
    from flask import g
    return getattr(g, 'current_user_id', None)


def get_current_user_role():
    """
    Récupère le rôle de l'utilisateur actuel depuis le contexte Flask
    
    Returns:
        Rôle de l'utilisateur ou None
    """
    from flask import g
    return getattr(g, 'current_user_role', None)


def optional_auth(f):
    """
    Décorateur pour une authentification optionnelle
    Si un token est fourni, il est vérifié et l'utilisateur est ajouté au contexte
    Si aucun token n'est fourni, la fonction continue sans utilisateur
    
    Usage:
        @optional_auth
        def optional_route():
            # user peut être None ou contenir les infos utilisateur
            user = get_current_user()
            pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Récupérer le token depuis l'en-tête Authorization
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            # Extraire le token (format: "Bearer <token>")
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                # Token mal formaté, continuer sans authentification
                pass
            else:
                # Vérifier le token
                auth_service = AuthService()
                token_data = auth_service.verify_token(token)
                
                if token_data:
                    # Ajouter les informations utilisateur à la requête
                    from flask import g
                    g.current_user = token_data['user']
                    g.current_user_id = token_data['user_id']
                    g.current_user_role = token_data['role']
        
        return f(*args, **kwargs)
    
    return decorated
