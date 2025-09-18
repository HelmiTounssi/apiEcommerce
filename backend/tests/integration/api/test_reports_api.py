"""
Tests pour l'API des rapports
"""

import pytest
from unittest.mock import Mock, patch
from src.service.impl.reports_service import ReportsService

class TestReportsAPI:
    """Tests pour l'API des rapports"""
    
    def test_generate_sales_report_success(self, client, auth_headers):
        """Test de génération du rapport des ventes"""
        with patch('src.service.impl.reports_service.ReportsService.generate_sales_report') as mock_reports:
            mock_reports.return_value = {
                'total_sales': 1500.0,
                'total_orders': 25,
                'average_order': 60.0,
                'period': {
                    'start_date': '2025-01-01',
                    'end_date': '2025-01-31'
                },
                'sales_data': [
                    {'date': '2025-01-01', 'revenue': 100.0, 'count': 2},
                    {'date': '2025-01-02', 'revenue': 150.0, 'count': 3}
                ]
            }
            
            response = client.get('/api/reports/sales?start_date=2025-01-01&end_date=2025-01-31', 
                                headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['total_sales'] == 1500.0
            assert data['data']['total_orders'] == 25
            assert data['data']['average_order'] == 60.0
    
    def test_generate_top_clients_report_success(self, client, auth_headers):
        """Test de génération du rapport des top clients"""
        with patch('src.service.impl.reports_service.ReportsService.generate_top_clients_report') as mock_reports:
            mock_reports.return_value = {
                'period': {
                    'start_date': '2025-01-01',
                    'end_date': '2025-01-31'
                },
                'clients': [
                    {'id': 1, 'nom': 'Client 1', 'email': 'client1@example.com', 'order_count': 10, 'total_spent': 500.0},
                    {'id': 2, 'nom': 'Client 2', 'email': 'client2@example.com', 'order_count': 8, 'total_spent': 400.0}
                ]
            }
            
            response = client.get('/api/reports/top-clients?start_date=2025-01-01&end_date=2025-01-31&limit=10', 
                                headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert len(data['data']['clients']) == 2
            assert data['data']['clients'][0]['nom'] == 'Client 1'
            assert data['data']['clients'][0]['total_spent'] == 500.0
    
    def test_generate_top_products_report_success(self, client, auth_headers):
        """Test de génération du rapport des top produits"""
        with patch('src.service.impl.reports_service.ReportsService.generate_top_products_report') as mock_reports:
            mock_reports.return_value = {
                'period': {
                    'start_date': '2025-01-01',
                    'end_date': '2025-01-31'
                },
                'products': [
                    {'id': 1, 'nom': 'Produit 1', 'quantity_sold': 100, 'revenue': 1000.0},
                    {'id': 2, 'nom': 'Produit 2', 'quantity_sold': 80, 'revenue': 800.0}
                ]
            }
            
            response = client.get('/api/reports/top-products?start_date=2025-01-01&end_date=2025-01-31&limit=10', 
                                headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert len(data['data']['products']) == 2
            assert data['data']['products'][0]['nom'] == 'Produit 1'
            assert data['data']['products'][0]['quantity_sold'] == 100
    
    def test_generate_orders_analysis_report_success(self, client, auth_headers):
        """Test de génération de l'analyse des commandes"""
        with patch('src.service.impl.reports_service.ReportsService.generate_orders_analysis_report') as mock_reports:
            mock_reports.return_value = {
                'period': {
                    'start_date': '2025-01-01',
                    'end_date': '2025-01-31'
                },
                'status_analysis': [
                    {'statut': 'en_attente', 'count': 5},
                    {'statut': 'validée', 'count': 15},
                    {'statut': 'expédiée', 'count': 10},
                    {'statut': 'annulée', 'count': 2}
                ],
                'temporal_analysis': [
                    {'date': '2025-01-01', 'count': 3},
                    {'date': '2025-01-02', 'count': 5}
                ]
            }
            
            response = client.get('/api/reports/orders-analysis?start_date=2025-01-01&end_date=2025-01-31', 
                                headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert len(data['data']['status_analysis']) == 4
            assert len(data['data']['temporal_analysis']) == 2
            assert data['data']['status_analysis'][0]['statut'] == 'en_attente'
    
    def test_generate_performance_report_success(self, client, auth_headers):
        """Test de génération du rapport de performance"""
        with patch('src.service.impl.reports_service.ReportsService.generate_performance_report') as mock_reports:
            mock_reports.return_value = {
                'period': {
                    'start_date': '2025-01-01',
                    'end_date': '2025-01-31'
                },
                'avg_response_time': 150.0,
                'requests_per_minute': 45,
                'error_rate': 0.5,
                'performance_data': [
                    {'date': '2025-01-01', 'response_time': 140.0, 'requests_per_minute': 40, 'error_rate': 0.3},
                    {'date': '2025-01-02', 'response_time': 160.0, 'requests_per_minute': 50, 'error_rate': 0.7}
                ]
            }
            
            response = client.get('/api/reports/performance?start_date=2025-01-01&end_date=2025-01-31', 
                                headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['avg_response_time'] == 150.0
            assert data['data']['requests_per_minute'] == 45
            assert data['data']['error_rate'] == 0.5
    
    def test_generate_report_general_success(self, client, auth_headers):
        """Test de génération de rapport général"""
        with patch('src.service.impl.reports_service.ReportsService.generate_sales_report') as mock_reports:
            mock_reports.return_value = {
                'total_sales': 1500.0,
                'total_orders': 25,
                'average_order': 60.0
            }
            
            response = client.get('/api/reports/generate?type=sales&start_date=2025-01-01&end_date=2025-01-31', 
                                headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['total_sales'] == 1500.0
    
    def test_generate_report_invalid_type(self, client, auth_headers):
        """Test de génération de rapport avec type invalide"""
        response = client.get('/api/reports/generate?type=invalid&start_date=2025-01-01&end_date=2025-01-31', 
                            headers=auth_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
        assert 'Type de rapport non supporté' in data['message']
    
    def test_generate_report_missing_type(self, client, auth_headers):
        """Test de génération de rapport sans type"""
        response = client.get('/api/reports/generate?start_date=2025-01-01&end_date=2025-01-31', 
                            headers=auth_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
        assert 'Type de rapport manquant' in data['message']
    
    def test_export_report_csv_success(self, client, auth_headers):
        """Test d'export de rapport en CSV"""
        with patch('src.service.impl.reports_service.ReportsService.export_report') as mock_reports:
            mock_csv = "Date,Ventes,Commandes,Panier Moyen\n2025-01-01,100.0,2,50.0\n2025-01-02,150.0,3,50.0"
            mock_reports.return_value = mock_csv
            
            response = client.get('/api/reports/export?type=sales&format=csv&start_date=2025-01-01&end_date=2025-01-31', 
                                headers=auth_headers)
            
            assert response.status_code == 200
            assert response.headers['Content-Type'] == 'text/csv'
            assert 'attachment' in response.headers['Content-Disposition']
            assert 'sales_report.csv' in response.headers['Content-Disposition']
    
    def test_export_report_json_success(self, client, auth_headers):
        """Test d'export de rapport en JSON"""
        with patch('src.service.impl.reports_service.ReportsService.export_report') as mock_reports:
            mock_json = {'total_sales': 1500.0, 'total_orders': 25}
            mock_reports.return_value = mock_json
            
            response = client.get('/api/reports/export?type=sales&format=json&start_date=2025-01-01&end_date=2025-01-31', 
                                headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['total_sales'] == 1500.0
    
    def test_export_report_pdf_success(self, client, auth_headers):
        """Test d'export de rapport en PDF"""
        with patch('src.service.impl.reports_service.ReportsService.export_report') as mock_reports:
            mock_pdf = b"PDF content simulation"
            mock_reports.return_value = mock_pdf
            
            response = client.get('/api/reports/export?type=sales&format=pdf&start_date=2025-01-01&end_date=2025-01-31', 
                                headers=auth_headers)
            
            assert response.status_code == 200
            assert response.headers['Content-Type'] == 'application/pdf'
            assert 'attachment' in response.headers['Content-Disposition']
            assert 'sales_report.pdf' in response.headers['Content-Disposition']
    
    def test_get_scheduled_reports_success(self, client, auth_headers):
        """Test de récupération des rapports programmés"""
        with patch('src.service.impl.reports_service.ReportsService.get_scheduled_reports') as mock_reports:
            mock_reports.return_value = [
                {
                    'id': 1,
                    'name': 'Rapport Ventes Quotidien',
                    'type': 'sales',
                    'schedule': 'daily',
                    'time': '08:00',
                    'enabled': True,
                    'recipients': ['admin@example.com']
                },
                {
                    'id': 2,
                    'name': 'Rapport Performance Hebdomadaire',
                    'type': 'performance',
                    'schedule': 'weekly',
                    'day': 'monday',
                    'time': '09:00',
                    'enabled': True,
                    'recipients': ['admin@example.com', 'manager@example.com']
                }
            ]
            
            response = client.get('/api/reports/scheduled', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert len(data['data']) == 2
            assert data['data'][0]['name'] == 'Rapport Ventes Quotidien'
            assert data['data'][0]['schedule'] == 'daily'
    
    def test_create_scheduled_report_success(self, client, admin_headers):
        """Test de création d'un rapport programmé"""
        report_data = {
            'name': 'Nouveau Rapport',
            'type': 'sales',
            'schedule': 'daily',
            'time': '10:00',
            'enabled': True,
            'recipients': ['admin@example.com']
        }
        
        with patch('src.service.impl.reports_service.ReportsService.create_scheduled_report') as mock_reports:
            mock_reports.return_value = {
                'id': 999,
                'name': 'Nouveau Rapport',
                'type': 'sales',
                'schedule': 'daily',
                'enabled': True,
                'created_at': '2025-01-01T12:00:00'
            }
            
            response = client.post('/api/reports/scheduled', 
                                 json=report_data, 
                                 headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Rapport programmé créé avec succès' in data['message']
            assert data['data']['name'] == 'Nouveau Rapport'
    
    def test_create_scheduled_report_missing_data(self, client, admin_headers):
        """Test de création de rapport programmé sans données"""
        response = client.post('/api/reports/scheduled', 
                             json=None, 
                             headers=admin_headers)
        
        assert response.status_code == 400
        data = response.json
        assert data['success'] is False
        assert 'Données du rapport manquantes' in data['message']
    
    def test_update_scheduled_report_success(self, client, admin_headers):
        """Test de mise à jour d'un rapport programmé"""
        report_data = {
            'name': 'Rapport Modifié',
            'enabled': False
        }
        
        with patch('src.service.impl.reports_service.ReportsService.update_scheduled_report') as mock_reports:
            mock_reports.return_value = {
                'id': 1,
                'name': 'Rapport Modifié',
                'enabled': False,
                'updated_at': '2025-01-01T12:00:00'
            }
            
            response = client.put('/api/reports/scheduled/1', 
                                json=report_data, 
                                headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Rapport programmé mis à jour avec succès' in data['message']
            assert data['data']['name'] == 'Rapport Modifié'
    
    def test_delete_scheduled_report_success(self, client, admin_headers):
        """Test de suppression d'un rapport programmé"""
        with patch('src.service.impl.reports_service.ReportsService.delete_scheduled_report') as mock_reports:
            mock_reports.return_value = {
                'id': 1,
                'deleted': True,
                'deleted_at': '2025-01-01T12:00:00'
            }
            
            response = client.delete('/api/reports/scheduled/1', headers=admin_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'Rapport programmé supprimé avec succès' in data['message']
            assert data['data']['deleted'] is True
    
    def test_reports_service_error(self, client, auth_headers):
        """Test d'erreur du service rapports"""
        with patch('src.service.impl.reports_service.ReportsService.generate_sales_report') as mock_reports:
            mock_reports.side_effect = Exception("Erreur service")
            
            response = client.get('/api/reports/sales', headers=auth_headers)
            
            assert response.status_code == 500
            data = response.json
            assert data['success'] is False
            assert 'Erreur lors de la génération du rapport ventes' in data['message']
    
    def test_get_reports_unauthorized(self, client):
        """Test d'accès non autorisé aux rapports"""
        response = client.get('/api/reports/sales')
        
        assert response.status_code == 401
    
    def test_create_scheduled_report_unauthorized(self, client, auth_headers):
        """Test de création de rapport programmé non autorisée"""
        report_data = {'name': 'Test Report'}
        
        response = client.post('/api/reports/scheduled', 
                             json=report_data, 
                             headers=auth_headers)
        
        assert response.status_code == 403
