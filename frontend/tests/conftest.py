"""
Configuration des tests frontend
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Ajouter le chemin du frontend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def mock_session_state():
    """Mock de session_state Streamlit"""
    with patch('streamlit.session_state') as mock_session:
        mock_session.get.return_value = None
        mock_session.__setitem__ = Mock()
        mock_session.__getitem__ = Mock(return_value=None)
        yield mock_session


@pytest.fixture
def mock_api_client():
    """Mock du client API"""
    with patch('services.api_client.ApiClient') as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Configuration des réponses par défaut
        mock_instance.get.return_value = {"success": True, "data": []}
        mock_instance.post.return_value = {"success": True, "data": {}}
        mock_instance.put.return_value = {"success": True, "data": {}}
        mock_instance.delete.return_value = {"success": True, "data": {}}
        
        yield mock_instance


@pytest.fixture
def sample_user_data():
    """Données utilisateur de test"""
    return {
        "id": 1,
        "nom": "Test User",
        "email": "test@example.com",
        "role": "client"
    }


@pytest.fixture
def sample_product_data():
    """Données produit de test"""
    return {
        "id": 1,
        "nom": "Test Product",
        "description": "Test Description",
        "prix": 99.99,
        "stock": 10,
        "categorie": "Test Category"
    }


@pytest.fixture
def sample_order_data():
    """Données commande de test"""
    return {
        "id": 1,
        "utilisateur_id": 1,
        "statut": "en_attente",
        "total": 199.98,
        "date_creation": "2023-01-01T00:00:00"
    }


@pytest.fixture
def auth_token():
    """Token d'authentification de test"""
    return "test_token_123456789"


@pytest.fixture
def admin_token():
    """Token administrateur de test"""
    return "admin_token_123456789"


@pytest.fixture
def mock_streamlit():
    """Mock de Streamlit"""
    with patch('streamlit') as mock_st:
        # Configuration des mocks Streamlit
        mock_st.session_state = {}
        mock_st.write = Mock()
        mock_st.error = Mock()
        mock_st.success = Mock()
        mock_st.info = Mock()
        mock_st.warning = Mock()
        mock_st.selectbox = Mock(return_value="option1")
        mock_st.text_input = Mock(return_value="test_input")
        mock_st.number_input = Mock(return_value=1)
        mock_st.button = Mock(return_value=True)
        mock_st.columns = Mock(return_value=[Mock(), Mock()])
        mock_st.markdown = Mock()
        mock_st.container = Mock()
        mock_st.expander = Mock()
        mock_st.dataframe = Mock()
        mock_st.plotly_chart = Mock()
        mock_st.metric = Mock()
        
        yield mock_st
