"""
Configuration centralisée pour le frontend
"""

import os

# Configuration de l'API
BACKEND_URL = os.getenv('BACKEND_URL', 'https://localhost')

# Configuration Streamlit
STREAMLIT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
STREAMLIT_ADDRESS = os.getenv('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')

# Configuration de l'application
APP_NAME = "E-commerce API"
APP_VERSION = "2.0.0"
