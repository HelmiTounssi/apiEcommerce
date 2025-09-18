"""
Tests pour l'API des statistiques
"""

import pytest
from unittest.mock import Mock, patch
from src.service.impl.stats_service import StatsService

class TestStatsAPI:
    """Tests pour l'API des statistiques"""
    
    def test_get_general_stats_success(self, client, auth_headers):
        """Test de récupération des statistiques générales"""
        with patch('src.service.impl.stats_service.StatsService.get_general_stats') as mock_stats:
            mock_stats.return_value = {
                'users': {'total': 10, 'new_today': 2, 'active': 8},
                'products': {'total': 50, 'new_today': 5, 'low_stock': 3},
                'orders': {'total': 25, 'new_today': 3, 'pending': 2},
                'revenue': {'total': 1500.0, 'today': 150.0, 'this_month': 800.0}
            }
            
            response = client.get('/api/stats/', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert 'data' in data
            assert data['data']['users']['total'] == 10
            assert data['data']['products']['total'] == 50
            assert data['data']['orders']['total'] == 25
            assert data['data']['revenue']['total'] == 1500.0
    
    def test_get_user_stats_success(self, client, auth_headers):
        """Test de récupération des statistiques utilisateurs"""
        with patch('src.service.impl.stats_service.StatsService.get_user_stats') as mock_stats:
            mock_stats.return_value = {
                'total': 10,
                'new_today': 2,
                'active': 8
            }
            
            response = client.get('/api/stats/users', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['total'] == 10
            assert data['data']['new_today'] == 2
            assert data['data']['active'] == 8
    
    def test_get_product_stats_success(self, client, auth_headers):
        """Test de récupération des statistiques produits"""
        with patch('src.service.impl.stats_service.StatsService.get_product_stats') as mock_stats:
            mock_stats.return_value = {
                'total': 50,
                'new_today': 5,
                'low_stock': 3
            }
            
            response = client.get('/api/stats/products', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['total'] == 50
            assert data['data']['new_today'] == 5
            assert data['data']['low_stock'] == 3
    
    def test_get_order_stats_success(self, client, auth_headers):
        """Test de récupération des statistiques commandes"""
        with patch('src.service.impl.stats_service.StatsService.get_order_stats') as mock_stats:
            mock_stats.return_value = {
                'total': 25,
                'new_today': 3,
                'pending': 2
            }
            
            response = client.get('/api/stats/orders', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['total'] == 25
            assert data['data']['new_today'] == 3
            assert data['data']['pending'] == 2
    
    def test_get_revenue_stats_success(self, client, auth_headers):
        """Test de récupération des statistiques CA"""
        with patch('src.service.impl.stats_service.StatsService.get_revenue_stats') as mock_stats:
            mock_stats.return_value = {
                'total': 1500.0,
                'today': 150.0,
                'this_month': 800.0
            }
            
            response = client.get('/api/stats/revenue', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert data['data']['total'] == 1500.0
            assert data['data']['today'] == 150.0
            assert data['data']['this_month'] == 800.0
    
    def test_get_orders_chart_data_success(self, client, auth_headers):
        """Test de récupération des données graphique commandes"""
        with patch('src.service.impl.stats_service.StatsService.get_orders_chart_data') as mock_stats:
            mock_stats.return_value = [
                {'date': '2025-01-01', 'count': 5},
                {'date': '2025-01-02', 'count': 8},
                {'date': '2025-01-03', 'count': 3}
            ]
            
            response = client.get('/api/stats/charts/orders?days=30', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert len(data['data']) == 3
            assert data['data'][0]['date'] == '2025-01-01'
            assert data['data'][0]['count'] == 5
    
    def test_get_revenue_chart_data_success(self, client, auth_headers):
        """Test de récupération des données graphique CA"""
        with patch('src.service.impl.stats_service.StatsService.get_revenue_chart_data') as mock_stats:
            mock_stats.return_value = [
                {'date': '2025-01-01', 'revenue': 100.0},
                {'date': '2025-01-02', 'revenue': 150.0},
                {'date': '2025-01-03', 'revenue': 200.0}
            ]
            
            response = client.get('/api/stats/charts/revenue?days=30', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert len(data['data']) == 3
            assert data['data'][0]['date'] == '2025-01-01'
            assert data['data'][0]['revenue'] == 100.0
    
    def test_get_top_products_success(self, client, auth_headers):
        """Test de récupération des top produits"""
        with patch('src.service.impl.stats_service.StatsService.get_top_products') as mock_stats:
            mock_stats.return_value = [
                {'id': 1, 'nom': 'Produit 1', 'quantity_sold': 100, 'revenue': 1000.0},
                {'id': 2, 'nom': 'Produit 2', 'quantity_sold': 80, 'revenue': 800.0}
            ]
            
            response = client.get('/api/stats/top-products?limit=10', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert len(data['data']) == 2
            assert data['data'][0]['nom'] == 'Produit 1'
            assert data['data'][0]['quantity_sold'] == 100
    
    def test_get_orders_by_status_success(self, client, auth_headers):
        """Test de récupération des commandes par statut"""
        with patch('src.service.impl.stats_service.StatsService.get_orders_by_status') as mock_stats:
            mock_stats.return_value = [
                {'statut': 'en_attente', 'count': 5},
                {'statut': 'validée', 'count': 10},
                {'statut': 'expédiée', 'count': 8},
                {'statut': 'annulée', 'count': 2}
            ]
            
            response = client.get('/api/stats/orders-by-status', headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json
            assert data['success'] is True
            assert len(data['data']) == 4
            assert data['data'][0]['statut'] == 'en_attente'
            assert data['data'][0]['count'] == 5
    
    def test_get_stats_unauthorized(self, client):
        """Test d'accès non autorisé aux statistiques"""
        response = client.get('/api/stats/')
        
        assert response.status_code == 401
    
    def test_get_stats_service_error(self, client, auth_headers):
        """Test d'erreur du service statistiques"""
        with patch('src.service.impl.stats_service.StatsService.get_general_stats') as mock_stats:
            mock_stats.side_effect = Exception("Erreur service")
            
            response = client.get('/api/stats/', headers=auth_headers)
            
            assert response.status_code == 500
            data = response.json
            assert data['success'] is False
            assert 'Erreur lors de la récupération des statistiques' in data['message']
    
    def test_get_orders_chart_invalid_days(self, client, auth_headers):
        """Test avec paramètre days invalide"""
        with patch('src.service.impl.stats_service.StatsService.get_orders_chart_data') as mock_stats:
            mock_stats.return_value = []
            
            response = client.get('/api/stats/charts/orders?days=invalid', headers=auth_headers)
            
            # Le paramètre invalide devrait être ignoré et utiliser la valeur par défaut
            assert response.status_code == 200
    
    def test_get_top_products_invalid_limit(self, client, auth_headers):
        """Test avec paramètre limit invalide"""
        with patch('src.service.impl.stats_service.StatsService.get_top_products') as mock_stats:
            mock_stats.return_value = []
            
            response = client.get('/api/stats/top-products?limit=invalid', headers=auth_headers)
            
            # Le paramètre invalide devrait être ignoré et utiliser la valeur par défaut
            assert response.status_code == 200
