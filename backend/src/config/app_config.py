"""
Configuration de l'application
"""

import os
from datetime import timedelta


class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://ecommerce_user:ecommerce_password_2025@postgres:5432/ecommerce'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Configuration JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token expire après 1 heure
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token expire après 30 jours
    JWT_EXPIRATION = 3600  # 1 heure en secondes


class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://ecommerce_user:ecommerce_password_2025@postgres:5432/ecommerce'


class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://ecommerce_user:ecommerce_password_2025@postgres:5432/ecommerce'


class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
