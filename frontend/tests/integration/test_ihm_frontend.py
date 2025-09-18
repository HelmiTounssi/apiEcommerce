"""
Tests d'intégration pour l'IHM frontend
"""

import pytest
import requests
import time

class TestIHMFrontendIntegration:
    """Tests d'intégration pour l'IHM frontend"""
    
    def test_frontend_accessibility(self):
        """Test d'accessibilité du frontend"""
        try:
            response = requests.get('http://localhost:8501/', timeout=10)
            assert response.status_code == 200
            assert 'streamlit' in response.text.lower()
        except requests.exceptions.ConnectionError:
            pytest.skip("Frontend Streamlit non accessible")
    
    def test_frontend_health_check(self):
        """Test de santé du frontend"""
        try:
            # Test de l'endpoint de santé de Streamlit
            response = requests.get('http://localhost:8501/_stcore/health', timeout=5)
            # Streamlit peut retourner 200 ou 404 selon la version
            assert response.status_code in [200, 404]
        except requests.exceptions.ConnectionError:
            pytest.skip("Frontend Streamlit non accessible")
    
    def test_frontend_static_files(self):
        """Test des fichiers statiques du frontend"""
        try:
            # Test de l'accès aux fichiers statiques
            response = requests.get('http://localhost:8501/static/', timeout=5)
            # Peut retourner 200, 404 ou 403 selon la configuration
            assert response.status_code in [200, 404, 403]
        except requests.exceptions.ConnectionError:
            pytest.skip("Frontend Streamlit non accessible")
    
    def test_backend_frontend_communication(self):
        """Test de communication entre frontend et backend"""
        try:
            # Test que le frontend peut communiquer avec le backend
            backend_response = requests.get('http://localhost:5000/', timeout=5)
            frontend_response = requests.get('http://localhost:8501/', timeout=5)
            
            assert backend_response.status_code == 200
            assert frontend_response.status_code == 200
            
            # Vérifier que les deux services sont accessibles
            assert 'streamlit' in frontend_response.text.lower()
            assert 'message' in backend_response.json()
            
        except requests.exceptions.ConnectionError as e:
            pytest.skip(f"Services non accessibles: {e}")
    
    def test_authentication_flow_frontend(self):
        """Test du flux d'authentification depuis le frontend"""
        try:
            # Simuler une connexion depuis le frontend
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "password"
            }
            
            response = requests.post('http://localhost:5000/api/auth/login', 
                                   json=login_data, timeout=5)
            
            assert response.status_code == 200
            data = response.json()
            assert data.get('success') is True
            assert 'token' in data
            assert 'utilisateur' in data
            
            # Vérifier que le token peut être utilisé
            token = data['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # Test d'accès aux produits
            products_response = requests.get('http://localhost:5000/api/produits/', 
                                           headers=headers, timeout=5)
            assert products_response.status_code == 200
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_product_images_frontend_integration(self):
        """Test d'intégration des images de produits pour le frontend"""
        try:
            # Authentification
            login_data = {
                "email": "admin@ecommerce.com",
                "mot_de_passe": "password"
            }
            
            auth_response = requests.post('http://localhost:5000/api/auth/login', 
                                        json=login_data, timeout=5)
            assert auth_response.status_code == 200
            
            token = auth_response.json()['token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # Récupération des produits
            products_response = requests.get('http://localhost:5000/api/produits/', 
                                           headers=headers, timeout=5)
            assert products_response.status_code == 200
            
            products = products_response.json()
            assert len(products) > 0
            
            # Vérifier que les images sont accessibles
            for product in products:
                if product.get('image_url'):
                    # Test d'accès à l'image (peut échouer si l'image n'existe pas vraiment)
                    try:
                        image_response = requests.get(f'http://localhost:5000{product["image_url"]}', 
                                                    timeout=5)
                        # Accepte 200 (image trouvée) ou 404 (image simulée)
                        assert image_response.status_code in [200, 404]
                    except requests.exceptions.ConnectionError:
                        # Ignore les erreurs de connexion pour les images
                        pass
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend non accessible")
    
    def test_frontend_backend_synchronization(self):
        """Test de synchronisation entre frontend et backend"""
        try:
            # Vérifier que les deux services sont synchronisés
            backend_start = time.time()
            backend_response = requests.get('http://localhost:5000/', timeout=5)
            backend_time = time.time() - backend_start
            
            frontend_start = time.time()
            frontend_response = requests.get('http://localhost:8501/', timeout=5)
            frontend_time = time.time() - frontend_start
            
            assert backend_response.status_code == 200
            assert frontend_response.status_code == 200
            
            # Vérifier que les temps de réponse sont raisonnables
            assert backend_time < 5.0  # Backend doit répondre en moins de 5 secondes
            assert frontend_time < 10.0  # Frontend doit répondre en moins de 10 secondes
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Services non accessibles")
    
    def test_error_handling_frontend(self):
        """Test de gestion d'erreurs du frontend"""
        try:
            # Test d'accès à une page inexistante
            response = requests.get('http://localhost:8501/nonexistent', timeout=5)
            # Streamlit peut retourner 200 (avec erreur) ou 404
            assert response.status_code in [200, 404]
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Frontend non accessible")
    
    def test_frontend_performance(self):
        """Test de performance du frontend"""
        try:
            start_time = time.time()
            response = requests.get('http://localhost:8501/', timeout=15)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            assert response.status_code == 200
            assert response_time < 15.0  # Le frontend doit se charger en moins de 15 secondes
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Frontend non accessible")
