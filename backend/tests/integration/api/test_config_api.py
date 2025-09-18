"""
Tests pour l'API de configuration
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch
from src.service.impl.config_service import ConfigService

class TestConfigAPI:
    """Tests pour l'API de configuration"""
    
    def test_get_config_success(self, client, auth_headers):
        """Test de récupération de la configuration"""
        with patch('src.service.impl.config_service.ConfigService.get_current_config') as mock_config:
            mock_config.return_value = {
                'app_name': 'E-commerce API',
                'debug_mode': False,
                'maintenance_mode': False,
                'database': {'type': 'SQLite', 'pool_size': 10},
                'api': {'timeout': 30, 'max_requests_per_minute': 100},
                'security': {'jwt_expiration': 1, 'password_min_length': 8}
            }
            
            response = client.get('/api/config/', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['app_name'] == 'E-commerce API'
            assert data['data']['debug_mode'] is False
    
    def test_update_config_success(self, client, admin_headers):
        """Test de mise à jour de la configuration"""
        config_data = {
            'app_name': 'Nouveau Nom API',
            'debug_mode': True,
            'database': {'pool_size': 20}
        }
        
        with patch('src.service.impl.config_service.ConfigService.update_config') as mock_config:
            mock_config.return_value = {
                'app_name': 'Nouveau Nom API',
                'debug_mode': True,
                'database': {'pool_size': 20}
            }
            
            response = client.post('/api/config/', 
                                 json=config_data, 
                                 headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Configuration mise à jour avec succès' in data['message']
    
    def test_update_config_unauthorized(self, client, auth_headers):
        """Test de mise à jour non autorisée"""
        config_data = {'app_name': 'Nouveau Nom'}
        
        response = client.post('/api/config/', 
                             json=config_data, 
                             headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_update_config_missing_data(self, client, admin_headers):
        """Test de mise à jour sans données"""
        response = client.post('/api/config/', 
                             json=None, 
                             headers=admin_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
        assert 'Données de configuration manquantes' in data['message']
    
    def test_get_app_config_success(self, client, auth_headers):
        """Test de récupération de la config app"""
        with patch('src.service.impl.config_service.ConfigService.get_app_config') as mock_config:
            mock_config.return_value = {
                'app_name': 'E-commerce API',
                'debug_mode': False,
                'maintenance_mode': False
            }
            
            response = client.get('/api/config/app', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['app_name'] == 'E-commerce API'
    
    def test_update_app_config_success(self, client, admin_headers):
        """Test de mise à jour de la config app"""
        app_data = {
            'app_name': 'Nouveau Nom',
            'debug_mode': True
        }
        
        with patch('src.service.impl.config_service.ConfigService.update_app_config') as mock_config:
            mock_config.return_value = app_data
            
            response = client.post('/api/config/app', 
                                 json=app_data, 
                                 headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
    
    def test_get_database_config_success(self, client, auth_headers):
        """Test de récupération de la config DB"""
        with patch('src.service.impl.config_service.ConfigService.get_database_config') as mock_config:
            mock_config.return_value = {
                'type': 'SQLite',
                'pool_size': 10,
                'timeout': 30
            }
            
            response = client.get('/api/config/database', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['type'] == 'SQLite'
    
    def test_update_database_config_success(self, client, admin_headers):
        """Test de mise à jour de la config DB"""
        db_data = {
            'type': 'PostgreSQL',
            'pool_size': 20
        }
        
        with patch('src.service.impl.config_service.ConfigService.update_database_config') as mock_config:
            mock_config.return_value = db_data
            
            response = client.post('/api/config/database', 
                                 json=db_data, 
                                 headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
    
    def test_get_api_config_success(self, client, auth_headers):
        """Test de récupération de la config API"""
        with patch('src.service.impl.config_service.ConfigService.get_api_config') as mock_config:
            mock_config.return_value = {
                'timeout': 30,
                'max_requests_per_minute': 100,
                'cors_enabled': True
            }
            
            response = client.get('/api/config/api', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['timeout'] == 30
    
    def test_update_api_config_success(self, client, admin_headers):
        """Test de mise à jour de la config API"""
        api_data = {
            'timeout': 60,
            'max_requests_per_minute': 200
        }
        
        with patch('src.service.impl.config_service.ConfigService.update_api_config') as mock_config:
            mock_config.return_value = api_data
            
            response = client.post('/api/config/api', 
                                 json=api_data, 
                                 headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
    
    def test_get_security_config_success(self, client, auth_headers):
        """Test de récupération de la config sécurité"""
        with patch('src.service.impl.config_service.ConfigService.get_security_config') as mock_config:
            mock_config.return_value = {
                'jwt_expiration': 1,
                'password_min_length': 8,
                'password_require_special': True
            }
            
            response = client.get('/api/config/security', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['jwt_expiration'] == 1
    
    def test_update_security_config_success(self, client, admin_headers):
        """Test de mise à jour de la config sécurité"""
        security_data = {
            'jwt_expiration': 2,
            'password_min_length': 10
        }
        
        with patch('src.service.impl.config_service.ConfigService.update_security_config') as mock_config:
            mock_config.return_value = security_data
            
            response = client.post('/api/config/security', 
                                 json=security_data, 
                                 headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
    
    def test_reset_config_success(self, client, admin_headers):
        """Test de réinitialisation de la configuration"""
        with patch('src.service.impl.config_service.ConfigService.reset_to_default') as mock_config:
            mock_config.return_value = {
                'app_name': 'E-commerce API',
                'debug_mode': False
            }
            
            response = client.post('/api/config/reset', headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Configuration réinitialisée' in data['message']
    
    def test_backup_config_success(self, client, admin_headers):
        """Test de sauvegarde de la configuration"""
        with patch('src.service.impl.config_service.ConfigService.backup_config') as mock_config:
            mock_config.return_value = {
                'backup_file': 'config_backup_20250101_120000.json',
                'backup_date': '2025-01-01T12:00:00',
                'config': {'app_name': 'E-commerce API'}
            }
            
            response = client.post('/api/config/backup', headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Configuration sauvegardée' in data['message']
    
    def test_restore_config_success(self, client, admin_headers):
        """Test de restauration de la configuration"""
        backup_data = {
            'config': {
                'app_name': 'E-commerce API',
                'debug_mode': False
            },
            'backup_date': '2025-01-01T12:00:00'
        }
        
        with patch('src.service.impl.config_service.ConfigService.restore_config') as mock_config:
            mock_config.return_value = backup_data['config']
            
            response = client.put('/api/config/backup', 
                                json=backup_data, 
                                headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Configuration restaurée' in data['message']
    
    def test_restore_config_missing_data(self, client, admin_headers):
        """Test de restauration sans données"""
        response = client.put('/api/config/backup', 
                            json=None, 
                            headers=admin_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
        assert 'Données de sauvegarde manquantes' in data['message']
    
    def test_config_service_error(self, client, auth_headers):
        """Test d'erreur du service configuration"""
        with patch('src.service.impl.config_service.ConfigService.get_current_config') as mock_config:
            mock_config.side_effect = Exception("Erreur service")
            
            response = client.get('/api/config/', headers=auth_headers)
            
            assert response.status_code == 500
            data = response.json
            assert data['success'] is False
            assert 'Erreur lors de la récupération de la configuration' in data['message']
    
    def test_get_config_unauthorized(self, client):
        """Test d'accès non autorisé à la configuration"""
        response = client.get('/api/config/')
        
        assert response.status_code == 401
