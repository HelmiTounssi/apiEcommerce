"""
Configuration centralisée pour le frontend
"""

import os

# Configuration de l'API
# En Docker, utilise le service backend directement, sinon localhost pour le développement local
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5000' if os.getenv('DOCKER_ENV') else 'https://localhost')

# Configuration Streamlit
STREAMLIT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
STREAMLIT_ADDRESS = os.getenv('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')

# Configuration de l'application
APP_NAME = "E-commerce API"
APP_VERSION = "2.0.0"
