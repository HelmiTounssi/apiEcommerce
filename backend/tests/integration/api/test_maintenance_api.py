"""
Tests pour l'API de maintenance
"""

import pytest
from unittest.mock import Mock, patch
from src.service.impl.maintenance_service import MaintenanceService

class TestMaintenanceAPI:
    """Tests pour l'API de maintenance"""
    
    def test_optimize_database_success(self, client, admin_headers):
        """Test d'optimisation de la base de données"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.optimize_database') as mock_maintenance:
            mock_maintenance.return_value = {
                'success': True,
                'message': 'Base de données optimisée avec succès',
                'duration_seconds': 2.5,
                'timestamp': '2025-01-01T12:00:00'
            }
            
            response = client.post('/api/maintenance/optimize-db', headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Base de données optimisée avec succès' in data['message']
    
    def test_optimize_database_unauthorized(self, client, auth_headers):
        """Test d'optimisation non autorisée"""
        response = client.post('/api/maintenance/optimize-db', headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_cleanup_temp_data_success(self, client, admin_headers):
        """Test de nettoyage des données temporaires"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.cleanup_temp_data') as mock_maintenance:
            mock_maintenance.return_value = {
                'success': True,
                'message': 'Données temporaires nettoyées avec succès',
                'cleaned_items': {
                    'temp_files': 5,
                    'old_logs': 10,
                    'expired_sessions': 3,
                    'cache': 2
                },
                'duration_seconds': 1.2,
                'timestamp': '2025-01-01T12:00:00'
            }
            
            response = client.post('/api/maintenance/cleanup', headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Données temporaires nettoyées avec succès' in data['message']
            assert data['data']['cleaned_items']['temp_files'] == 5
    
    def test_analyze_performance_success(self, client, auth_headers):
        """Test d'analyse des performances"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.analyze_performance') as mock_maintenance:
            mock_maintenance.return_value = {
                'system': {
                    'cpu_percent': 25.5,
                    'memory_percent': 60.0,
                    'disk_percent': 45.0,
                    'load_average': [1.2, 1.5, 1.8]
                },
                'database': {
                    'connection_count': 5,
                    'query_count': 1000,
                    'avg_query_time': 15.5,
                    'cache_hit_ratio': 0.95
                },
                'application': {
                    'active_requests': 10,
                    'total_requests': 5000,
                    'error_rate': 0.5,
                    'response_time_avg': 120.0
                },
                'timestamp': '2025-01-01T12:00:00'
            }
            
            response = client.get('/api/maintenance/performance', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['system']['cpu_percent'] == 25.5
            assert data['data']['database']['connection_count'] == 5
            assert data['data']['application']['active_requests'] == 10
    
    def test_restart_api_success(self, client, admin_headers):
        """Test de redémarrage de l'API"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.restart_api') as mock_maintenance:
            mock_maintenance.return_value = {
                'success': True,
                'message': 'API redémarrée avec succès',
                'timestamp': '2025-01-01T12:00:00',
                'note': 'Redémarrage simulé'
            }
            
            response = client.post('/api/maintenance/restart', headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'API redémarrée avec succès' in data['message']
    
    def test_restart_cache_success(self, client, admin_headers):
        """Test de redémarrage du cache"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.restart_cache') as mock_maintenance:
            mock_maintenance.return_value = {
                'success': True,
                'message': 'Cache redémarré avec succès',
                'timestamp': '2025-01-01T12:00:00'
            }
            
            response = client.post('/api/maintenance/restart-cache', headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Cache redémarré avec succès' in data['message']
    
    def test_get_system_logs_success(self, client, auth_headers):
        """Test de récupération des logs système"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.get_system_logs') as mock_maintenance:
            mock_logs = """2025-01-01 12:00:00 - INFO - Application démarrée
2025-01-01 12:01:00 - INFO - Base de données connectée
2025-01-01 12:02:00 - WARNING - Cache presque plein"""
            
            mock_maintenance.return_value = mock_logs
            
            response = client.get('/api/maintenance/logs?level=INFO&lines=100', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Application démarrée' in data['data']
    
    def test_get_system_logs_default_params(self, client, auth_headers):
        """Test de récupération des logs avec paramètres par défaut"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.get_system_logs') as mock_maintenance:
            mock_maintenance.return_value = "Log entry 1\nLog entry 2"
            
            response = client.get('/api/maintenance/logs', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
    
    def test_health_check_success(self, client):
        """Test de vérification de santé"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.health_check') as mock_maintenance:
            mock_maintenance.return_value = {
                'overall_status': 'healthy',
                'checks': {
                    'database': {'status': 'healthy', 'message': 'Base de données accessible'},
                    'disk': {'status': 'healthy', 'message': 'Espace disque OK: 45.2%'},
                    'memory': {'status': 'healthy', 'message': 'Mémoire OK: 60.0%'},
                    'performance': {'status': 'healthy', 'message': 'Performances normales'}
                }
            }
            
            response = client.get('/api/maintenance/health')
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['overall_status'] == 'healthy'
            assert data['data']['checks']['database']['status'] == 'healthy'
    
    def test_health_check_degraded(self, client):
        """Test de vérification de santé dégradée"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.health_check') as mock_maintenance:
            mock_maintenance.return_value = {
                'overall_status': 'degraded',
                'checks': {
                    'database': {'status': 'healthy', 'message': 'Base de données accessible'},
                    'disk': {'status': 'degraded', 'message': 'Espace disque faible: 85.0%'},
                    'memory': {'status': 'healthy', 'message': 'Mémoire OK: 60.0%'},
                    'performance': {'status': 'healthy', 'message': 'Performances normales'}
                }
            }
            
            response = client.get('/api/maintenance/health')
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['overall_status'] == 'degraded'
    
    def test_get_system_status_success(self, client, auth_headers):
        """Test de récupération du statut système"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.get_system_status') as mock_maintenance:
            mock_maintenance.return_value = {
                'uptime': '2h 30m',
                'version': '1.0.0',
                'environment': 'development',
                'database_status': 'connected',
                'cache_status': 'active',
                'api_status': 'running',
                'timestamp': '2025-01-01T12:00:00'
            }
            
            response = client.get('/api/maintenance/status', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['uptime'] == '2h 30m'
            assert data['data']['version'] == '1.0.0'
            assert data['data']['api_status'] == 'running'
    
    def test_backup_system_success(self, client, admin_headers):
        """Test de sauvegarde du système"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.backup_system') as mock_maintenance:
            mock_maintenance.return_value = {
                'success': True,
                'message': 'Sauvegarde full effectuée avec succès',
                'backup_info': {
                    'type': 'full',
                    'start_time': '2025-01-01T12:00:00',
                    'end_time': '2025-01-01T12:05:00',
                    'duration_seconds': 300.0,
                    'files': ['database_backup.sql', 'config_backup.json', 'logs_backup.tar.gz']
                }
            }
            
            response = client.post('/api/maintenance/backup?type=full', headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Sauvegarde full effectuée avec succès' in data['message']
            assert len(data['data']['backup_info']['files']) == 3
    
    def test_backup_system_database_only(self, client, admin_headers):
        """Test de sauvegarde base de données seulement"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.backup_system') as mock_maintenance:
            mock_maintenance.return_value = {
                'success': True,
                'message': 'Sauvegarde database effectuée avec succès',
                'backup_info': {
                    'type': 'database',
                    'files': ['database_backup.sql']
                }
            }
            
            response = client.post('/api/maintenance/backup?type=database', headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['backup_info']['type'] == 'database'
    
    def test_restore_system_success(self, client, admin_headers):
        """Test de restauration du système"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.restore_system') as mock_maintenance:
            mock_maintenance.return_value = {
                'success': True,
                'message': 'Système restauré depuis backup_20250101_120000.sql',
                'timestamp': '2025-01-01T12:00:00',
                'note': 'Restauration simulée'
            }
            
            response = client.post('/api/maintenance/restore?backup_file=backup_20250101_120000.sql', 
                                 headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Système restauré depuis' in data['message']
    
    def test_restore_system_missing_file(self, client, admin_headers):
        """Test de restauration sans fichier de sauvegarde"""
        response = client.post('/api/maintenance/restore', headers=admin_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
        assert 'Fichier de sauvegarde manquant' in data['message']
    
    def test_maintenance_service_error(self, client, admin_headers):
        """Test d'erreur du service maintenance"""
        with patch('src.service.impl.maintenance_service.MaintenanceService.optimize_database') as mock_maintenance:
            mock_maintenance.side_effect = Exception("Erreur service")
            
            response = client.post('/api/maintenance/optimize-db', headers=admin_headers)
            
            assert response.status_code == 500
            data = response.json
            assert data['success'] is False
            assert 'Erreur lors de l\'optimisation' in data['message']
    
    def test_analyze_performance_unauthorized(self, client):
        """Test d'analyse des performances non autorisée"""
        response = client.get('/api/maintenance/performance')
        
        assert response.status_code == 401
    
    def test_get_system_logs_unauthorized(self, client):
        """Test de récupération des logs non autorisée"""
        response = client.get('/api/maintenance/logs')
        
        assert response.status_code == 401
