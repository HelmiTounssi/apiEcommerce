#!/usr/bin/env python3
"""
Script principal de démarrage pour l'API E-commerce
Architecture en Couches
"""

import sys
import os

# Ajouter le répertoire src au path Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import create_app, init_db

if __name__ == '__main__':
    print("🚀 Démarrage de l'API E-commerce avec Architecture en Couches...")
    print("📊 Base de données SQLite avec SQLAlchemy")
    print("🏗️  Architecture: Layered Architecture")
    print("🌐 Serveur disponible sur: http://localhost:5000")
    print("📚 Documentation Swagger: http://localhost:5000/docs/")
    print("🔧 Couches:")
    print("   - Domain: Entités métier et modèles")
    print("   - Data: Repositories et accès aux données")
    print("   - Service: Logique métier")
    print("   - Controller: Présentation et API")
    print("=" * 70)
    
    # Créer l'application
    app = create_app('development')
    
    # Initialiser la base de données
    init_db(app)
    
    # Démarrer l'application
    app.run(debug=True, host='0.0.0.0', port=5000)

