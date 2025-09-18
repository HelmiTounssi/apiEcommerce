"""
Middleware de logging pour les requêtes API
"""

import time
import json
from functools import wraps
from flask import request, g, current_app
from typing import Optional, Dict, Any
from .logging_config import api_requests_logger, get_logger

logger = get_logger(__name__)


def log_api_request(method: str, endpoint: str, status_code: int, 
                   response_time: float, user_id: Optional[int] = None,
                   request_data: Optional[dict] = None, 
                   response_data: Optional[dict] = None,
                   error: Optional[str] = None):
    """
    Log une requête API avec toutes les informations pertinentes
    
    Args:
        method: Méthode HTTP (GET, POST, etc.)
        endpoint: Endpoint de l'API
        status_code: Code de statut HTTP
        response_time: Temps de réponse en secondes
        user_id: ID de l'utilisateur (optionnel)
        request_data: Données de la requête (optionnel)
        response_data: Données de la réponse (optionnel)
        error: Message d'erreur (optionnel)
    """
    
    # Informations de base
    log_data = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'method': method,
        'endpoint': endpoint,
        'status_code': status_code,
        'response_time_ms': round(response_time * 1000, 2),
        'user_id': user_id
    }
    
    # Ajouter les données de requête si présentes
    if request_data:
        log_data['request_data'] = request_data
    
    # Ajouter les données de réponse si présentes
    if response_data:
        log_data['response_data'] = response_data
    
    # Ajouter l'erreur si présente
    if error:
        log_data['error'] = error
    
    # Log formaté
    api_requests_logger.info(json.dumps(log_data, ensure_ascii=False, indent=None))


def log_request_response(f):
    """
    Décorateur pour logger les requêtes et réponses API
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Informations de la requête
        start_time = time.time()
        method = request.method
        endpoint = request.endpoint or request.path
        user_agent = request.headers.get('User-Agent', 'Unknown')
        remote_addr = request.remote_addr
        session_id = request.headers.get('X-Session-ID', 'No-Session')
        
        # Récupérer l'ID utilisateur si disponible
        user_id = None
        if hasattr(g, 'current_user') and g.current_user:
            user_id = g.current_user.get('id')
        
        # Données de la requête
        request_data = None
        if request.is_json and request.get_json():
            request_data = request.get_json()
        elif request.form:
            request_data = dict(request.form)
        elif request.args:
            request_data = dict(request.args)
        
        # Log de la requête entrante
        logger.info(f"🔵 REQUEST | {method} {endpoint} | User: {user_id} | Session: {session_id} | IP: {remote_addr}")
        
        if request_data:
            logger.debug(f"📥 Request Data: {json.dumps(request_data, ensure_ascii=False, default=str)}")
        
        # Exécuter la fonction
        try:
            response = f(*args, **kwargs)
            response_time = time.time() - start_time
            
            # Déterminer le code de statut
            status_code = 200
            if isinstance(response, tuple):
                status_code = response[1] if len(response) > 1 else 200
                response_data = response[0] if len(response) > 0 else None
            else:
                response_data = response
            
            # Log de la réponse
            logger.info(f"🟢 RESPONSE | {method} {endpoint} | Status: {status_code} | Time: {response_time:.3f}s")
            
            if response_data and isinstance(response_data, dict):
                logger.debug(f"📤 Response Data: {json.dumps(response_data, ensure_ascii=False, default=str)}")
            
            # Log détaillé pour l'analyse
            log_api_request(
                method=method,
                endpoint=endpoint,
                status_code=status_code,
                response_time=response_time,
                user_id=user_id,
                request_data=request_data,
                response_data=response_data if isinstance(response_data, dict) else None
            )
            
            return response
            
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = str(e)
            
            # Log de l'erreur
            logger.error(f"🔴 ERROR | {method} {endpoint} | Error: {error_msg} | Time: {response_time:.3f}s")
            
            # Log détaillé de l'erreur
            log_api_request(
                method=method,
                endpoint=endpoint,
                status_code=500,
                response_time=response_time,
                user_id=user_id,
                request_data=request_data,
                error=error_msg
            )
            
            # Re-lever l'exception
            raise
    
    return decorated_function


def log_database_operation(operation: str, table: str, **kwargs):
    """
    Log une opération de base de données
    
    Args:
        operation: Type d'opération (SELECT, INSERT, UPDATE, DELETE)
        table: Nom de la table
        **kwargs: Informations supplémentaires
    """
    from .logging_config import log_database_operation as _log_db_op
    
    _log_db_op(
        operation=operation,
        table=table,
        record_id=kwargs.get('record_id'),
        data=kwargs.get('data'),
        error=kwargs.get('error')
    )


def log_business_operation(service: str, operation: str, **kwargs):
    """
    Log une opération métier
    
    Args:
        service: Nom du service
        operation: Nom de l'opération
        **kwargs: Informations supplémentaires
    """
    from .logging_config import log_business_operation as _log_business_op
    
    _log_business_op(
        service=service,
        operation=operation,
        user_id=kwargs.get('user_id'),
        data=kwargs.get('data'),
        result=kwargs.get('result'),
        error=kwargs.get('error')
    )


class RequestContext:
    """Contexte de requête pour le logging"""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_id = None
        self.user_id = None
        self.session_id = None
    
    def set_request_id(self, request_id: str):
        self.request_id = request_id
    
    def set_user_id(self, user_id: int):
        self.user_id = user_id
    
    def set_session_id(self, session_id: str):
        self.session_id = session_id
    
    def get_elapsed_time(self) -> float:
        return time.time() - self.start_time


def get_request_context() -> RequestContext:
    """Récupère le contexte de la requête courante"""
    if not hasattr(g, 'request_context'):
        g.request_context = RequestContext()
    return g.request_context


def log_performance_metrics(operation: str, duration: float, **kwargs):
    """
    Log des métriques de performance
    
    Args:
        operation: Nom de l'opération
        duration: Durée en secondes
        **kwargs: Métriques supplémentaires
    """
    metrics = {
        'operation': operation,
        'duration_ms': round(duration * 1000, 2),
        'timestamp': time.time()
    }
    metrics.update(kwargs)
    
    logger.info(f"📊 PERFORMANCE | {json.dumps(metrics, ensure_ascii=False)}")


def log_security_event(event_type: str, details: Dict[str, Any]):
    """
    Log un événement de sécurité
    
    Args:
        event_type: Type d'événement (login, logout, unauthorized_access, etc.)
        details: Détails de l'événement
    """
    security_data = {
        'event_type': event_type,
        'timestamp': time.time(),
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'details': details
    }
    
    logger.warning(f"🔒 SECURITY | {json.dumps(security_data, ensure_ascii=False)}")


def log_user_action(action: str, user_id: Optional[int] = None, **kwargs):
    """
    Log une action utilisateur
    
    Args:
        action: Action effectuée
        user_id: ID de l'utilisateur
        **kwargs: Informations supplémentaires
    """
    action_data = {
        'action': action,
        'user_id': user_id,
        'timestamp': time.time(),
        'ip_address': request.remote_addr,
        'session_id': request.headers.get('X-Session-ID', 'No-Session'),
        'details': kwargs
    }
    
    logger.info(f"👤 USER_ACTION | {json.dumps(action_data, ensure_ascii=False)}")
