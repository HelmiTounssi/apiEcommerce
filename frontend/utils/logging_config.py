"""
Configuration du logging pour le frontend Streamlit
"""

import logging
import logging.handlers
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
import streamlit as st


class StreamlitLogger:
    """Logger spécialisé pour Streamlit avec traçabilité complète"""
    
    def __init__(self, name: str = "ecommerce_frontend"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Initialiser l'attribut _api_calls_logger
        self._api_calls_logger = None
        
        # Éviter la duplication des handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configure les handlers de logging"""
        try:
            # 1. Handler console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-15s:%(lineno)-4d | %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
            # 2. Handler fichier pour tous les logs
            if not os.path.exists('logs'):
                os.makedirs('logs')
            
            file_handler = logging.handlers.RotatingFileHandler(
                'logs/frontend.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-15s:%(lineno)-4d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # 3. Handler fichier pour les erreurs uniquement
            error_handler = logging.handlers.RotatingFileHandler(
                'logs/frontend_errors.log',
                maxBytes=5*1024*1024,  # 5MB
                backupCount=3,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(file_formatter)
            self.logger.addHandler(error_handler)
            
            # 4. Handler fichier pour les appels API
            api_handler = logging.handlers.RotatingFileHandler(
                'logs/frontend_api_calls.log',
                maxBytes=20*1024*1024,  # 20MB
                backupCount=10,
                encoding='utf-8'
            )
            api_handler.setLevel(logging.INFO)
            api_formatter = logging.Formatter(
                '%(asctime)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            api_handler.setFormatter(api_formatter)
            
            # Logger spécialisé pour les appels API
            self._api_calls_logger = logging.getLogger(f"{self.logger.name}.api_calls")
            self._api_calls_logger.setLevel(logging.INFO)
            self._api_calls_logger.addHandler(api_handler)
            self._api_calls_logger.propagate = False  # Éviter la duplication
            
        except Exception as e:
            # En cas d'erreur, créer un logger de fallback
            print(f"⚠️ Erreur lors de la configuration du logging: {e}")
            self._api_calls_logger = logging.getLogger(f"{self.logger.name}.api_calls")
            self._api_calls_logger.setLevel(logging.INFO)
    
    def get_logger(self) -> logging.Logger:
        """Retourne le logger principal"""
        return self.logger
    
    def get_api_calls_logger(self) -> logging.Logger:
        """Retourne le logger spécialisé pour les appels API"""
        if self._api_calls_logger is None:
            # Créer un logger de fallback si l'initialisation a échoué
            self._api_calls_logger = logging.getLogger(f"{self.logger.name}.api_calls")
            self._api_calls_logger.setLevel(logging.INFO)
        return self._api_calls_logger


# Instance globale du logger
frontend_logger = StreamlitLogger()
logger = frontend_logger.get_logger()
api_calls_logger = frontend_logger.get_api_calls_logger()


def log_api_call(method: str, url: str, status_code: int, 
                response_time: float, request_data: Optional[dict] = None, 
                response_data: Optional[dict] = None, error: Optional[str] = None):
    """
    Log un appel API côté frontend
    
    Args:
        method: Méthode HTTP (GET, POST, etc.)
        url: URL de l'API
        status_code: Code de statut HTTP
        response_time: Temps de réponse en secondes
        request_data: Données de la requête (optionnel)
        response_data: Données de la réponse (optionnel)
        error: Message d'erreur (optionnel)
    """
    
    # Informations de base
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'url': url,
        'status_code': status_code,
        'response_time_ms': round(response_time * 1000, 2),
        'session_id': st.session_state.get('session_id', 'No-Session'),
        'user_authenticated': st.session_state.get('authenticated', False),
        'user_id': st.session_state.get('user_id', None)
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
    api_calls_logger.info(json.dumps(log_data, ensure_ascii=False, indent=None))


def log_user_action(action: str, **kwargs):
    """
    Log une action utilisateur dans l'IHM
    
    Args:
        action: Action effectuée
        **kwargs: Informations supplémentaires
    """
    
    action_data = {
        'action': action,
        'timestamp': datetime.now().isoformat(),
        'session_id': st.session_state.get('session_id', 'No-Session'),
        'user_authenticated': st.session_state.get('authenticated', False),
        'user_id': st.session_state.get('user_id', None),
        'page': st.session_state.get('selected_page', 'Unknown'),
        'details': kwargs
    }
    
    logger.info(f"👤 USER_ACTION | {json.dumps(action_data, ensure_ascii=False)}")


def log_navigation(from_page: str, to_page: str, **kwargs):
    """
    Log une navigation entre pages
    
    Args:
        from_page: Page de départ
        to_page: Page d'arrivée
        **kwargs: Informations supplémentaires
    """
    
    nav_data = {
        'navigation': f"{from_page} -> {to_page}",
        'timestamp': datetime.now().isoformat(),
        'session_id': st.session_state.get('session_id', 'No-Session'),
        'user_authenticated': st.session_state.get('authenticated', False),
        'user_id': st.session_state.get('user_id', None),
        'details': kwargs
    }
    
    logger.info(f"🧭 NAVIGATION | {json.dumps(nav_data, ensure_ascii=False)}")


def log_error(error: Exception, context: str = "", **kwargs):
    """
    Log une erreur avec contexte
    
    Args:
        error: Exception levée
        context: Contexte de l'erreur
        **kwargs: Informations supplémentaires
    """
    
    error_data = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context,
        'timestamp': datetime.now().isoformat(),
        'session_id': st.session_state.get('session_id', 'No-Session'),
        'user_authenticated': st.session_state.get('authenticated', False),
        'user_id': st.session_state.get('user_id', None),
        'page': st.session_state.get('selected_page', 'Unknown'),
        'details': kwargs
    }
    
    logger.error(f"❌ ERROR | {json.dumps(error_data, ensure_ascii=False)}")


def log_performance(operation: str, duration: float, **kwargs):
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
        'timestamp': datetime.now().isoformat(),
        'session_id': st.session_state.get('session_id', 'No-Session'),
        'details': kwargs
    }
    
    logger.info(f"📊 PERFORMANCE | {json.dumps(metrics, ensure_ascii=False)}")


def log_authentication_event(event_type: str, **kwargs):
    """
    Log un événement d'authentification
    
    Args:
        event_type: Type d'événement (login, logout, token_refresh, etc.)
        **kwargs: Informations supplémentaires
    """
    
    auth_data = {
        'event_type': event_type,
        'timestamp': datetime.now().isoformat(),
        'session_id': st.session_state.get('session_id', 'No-Session'),
        'details': kwargs
    }
    
    logger.info(f"🔐 AUTH | {json.dumps(auth_data, ensure_ascii=False)}")


# Fonction utilitaire pour créer des loggers spécialisés
def get_logger(name: str) -> logging.Logger:
    """
    Crée un logger spécialisé pour un module
    
    Args:
        name: Nom du logger (généralement __name__)
    
    Returns:
        Logger configuré
    """
    return logging.getLogger(f"ecommerce_frontend.{name}")


# Configuration des loggers externes
def configure_external_loggers():
    """Configure les loggers des bibliothèques externes"""
    
    # Réduire le niveau de logging des bibliothèques externes
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('streamlit').setLevel(logging.WARNING)


# Initialisation
configure_external_loggers()
