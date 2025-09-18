"""
Configuration centralisée du logging pour l'API backend
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Formateur de logs avec couleurs pour la console"""
    
    # Codes de couleur ANSI
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Vert
        'WARNING': '\033[33m',  # Jaune
        'ERROR': '\033[31m',    # Rouge
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Ajouter la couleur selon le niveau
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


class APILogger:
    """Logger spécialisé pour l'API avec traçabilité complète"""
    
    def __init__(self, name: str = "ecommerce_api"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Éviter la duplication des handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configure les handlers de logging"""
        
        # 1. Handler console avec couleurs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            '%(asctime)s | %(levelname)-8s | %(name)-20s | %(funcName)-15s:%(lineno)-4d | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # 2. Handler fichier pour tous les logs
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        file_handler = logging.handlers.RotatingFileHandler(
            'logs/api.log',
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
            'logs/errors.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        self.logger.addHandler(error_handler)
        
        # 4. Handler fichier pour les requêtes API
        api_handler = logging.handlers.RotatingFileHandler(
            'logs/api_requests.log',
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
        
        # Logger spécialisé pour les requêtes API
        self.api_requests_logger = logging.getLogger(f"{self.logger.name}.requests")
        self.api_requests_logger.setLevel(logging.INFO)
        self.api_requests_logger.addHandler(api_handler)
        self.api_requests_logger.propagate = False  # Éviter la duplication
    
    def get_logger(self) -> logging.Logger:
        """Retourne le logger principal"""
        return self.logger
    
    def get_api_requests_logger(self) -> logging.Logger:
        """Retourne le logger spécialisé pour les requêtes API"""
        return self.api_requests_logger


# Instance globale du logger
api_logger = APILogger()
logger = api_logger.get_logger()
api_requests_logger = api_logger.get_api_requests_logger()


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
        'timestamp': datetime.now().isoformat(),
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
    import json
    api_requests_logger.info(json.dumps(log_data, ensure_ascii=False, indent=None))


def log_database_operation(operation: str, table: str, record_id: Optional[int] = None,
                          data: Optional[dict] = None, error: Optional[str] = None):
    """
    Log une opération de base de données
    
    Args:
        operation: Type d'opération (SELECT, INSERT, UPDATE, DELETE)
        table: Nom de la table
        record_id: ID de l'enregistrement (optionnel)
        data: Données impliquées (optionnel)
        error: Message d'erreur (optionnel)
    """
    
    message = f"DB {operation} | Table: {table}"
    
    if record_id:
        message += f" | ID: {record_id}"
    
    if data:
        message += f" | Data: {data}"
    
    if error:
        message += f" | Error: {error}"
        logger.error(message)
    else:
        logger.debug(message)


def log_business_operation(service: str, operation: str, user_id: Optional[int] = None,
                          data: Optional[dict] = None, result: Optional[dict] = None,
                          error: Optional[str] = None):
    """
    Log une opération métier
    
    Args:
        service: Nom du service
        operation: Nom de l'opération
        user_id: ID de l'utilisateur (optionnel)
        data: Données d'entrée (optionnel)
        result: Résultat (optionnel)
        error: Message d'erreur (optionnel)
    """
    
    message = f"BUSINESS {service}.{operation}"
    
    if user_id:
        message += f" | User: {user_id}"
    
    if data:
        message += f" | Input: {data}"
    
    if result:
        message += f" | Result: {result}"
    
    if error:
        message += f" | Error: {error}"
        logger.error(message)
    else:
        logger.info(message)


# Fonction utilitaire pour créer des loggers spécialisés
def get_logger(name: str) -> logging.Logger:
    """
    Crée un logger spécialisé pour un module
    
    Args:
        name: Nom du logger (généralement __name__)
    
    Returns:
        Logger configuré
    """
    return logging.getLogger(f"ecommerce_api.{name}")


# Configuration des loggers externes
def configure_external_loggers():
    """Configure les loggers des bibliothèques externes"""
    
    # Réduire le niveau de logging des bibliothèques externes
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
    logging.getLogger('flask_migrate').setLevel(logging.WARNING)


# Initialisation
configure_external_loggers()
