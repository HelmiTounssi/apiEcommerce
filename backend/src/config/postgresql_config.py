"""
Configuration PostgreSQL optimisée pour l'e-commerce
"""

import os
from datetime import timedelta


class PostgreSQLConfig:
    """Configuration PostgreSQL pour la production"""
    
    # Configuration de base
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Configuration JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_EXPIRATION = 3600
    
    # Configuration PostgreSQL
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'ecommerce_db')
    DB_USER = os.environ.get('DB_USER', 'ecommerce_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'ecommerce_password')
    
    # URL de connexion PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Configuration de pool de connexions
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,                    # Nombre de connexions dans le pool
        'pool_recycle': 3600,               # Recycler les connexions après 1h
        'pool_pre_ping': True,              # Vérifier les connexions avant utilisation
        'max_overflow': 30,                 # Connexions supplémentaires en cas de pic
        'echo': False,                      # Désactiver les logs SQL en production
    }
    
    # Configuration Redis pour le cache
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Configuration Celery pour les tâches asynchrones
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')


class DevelopmentPostgreSQLConfig(PostgreSQLConfig):
    """Configuration PostgreSQL pour le développement"""
    DEBUG = True
    
    # Base de données de développement
    DB_NAME = os.environ.get('DB_NAME', 'ecommerce_dev')
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PostgreSQLConfig.DB_USER}:{PostgreSQLConfig.DB_PASSWORD}@{PostgreSQLConfig.DB_HOST}:{PostgreSQLConfig.DB_PORT}/{DB_NAME}"
    
    # Activer les logs SQL en développement
    SQLALCHEMY_ENGINE_OPTIONS = {
        **PostgreSQLConfig.SQLALCHEMY_ENGINE_OPTIONS,
        'echo': True,  # Activer les logs SQL
    }


class ProductionPostgreSQLConfig(PostgreSQLConfig):
    """Configuration PostgreSQL pour la production"""
    DEBUG = False
    
    # Configuration de sécurité
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Obligatoire en production
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')  # Obligatoire en production
    
    # Configuration de performance
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 50,                    # Plus de connexions en production
        'pool_recycle': 1800,               # Recycler plus souvent
        'pool_pre_ping': True,
        'max_overflow': 100,                # Plus de connexions en cas de pic
        'echo': False,
        'connect_args': {
            'connect_timeout': 10,
            'application_name': 'ecommerce_api',
        }
    }


class TestingPostgreSQLConfig(PostgreSQLConfig):
    """Configuration PostgreSQL pour les tests"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    
    # Base de données de test
    DB_NAME = os.environ.get('DB_NAME', 'ecommerce_test')
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PostgreSQLConfig.DB_USER}:{PostgreSQLConfig.DB_PASSWORD}@{PostgreSQLConfig.DB_HOST}:{PostgreSQLConfig.DB_PORT}/{DB_NAME}"
    
    # Configuration optimisée pour les tests
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'max_overflow': 10,
        'echo': False,
    }


# Configuration par environnement
postgresql_config = {
    'development': DevelopmentPostgreSQLConfig,
    'production': ProductionPostgreSQLConfig,
    'testing': TestingPostgreSQLConfig,
    'default': DevelopmentPostgreSQLConfig
}
