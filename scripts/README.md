# Scripts - API E-commerce Architecture en Couches

Ce répertoire contient tous les scripts utilitaires pour l'API E-commerce avec architecture en couches.

## 📁 Contenu du Répertoire

### 🚀 Scripts de Démarrage
- `start_layered.py` - Script Python pour démarrer l'API
- `start_layered.bat` - Script batch Windows pour démarrer l'API

### 🗄️ Scripts de Données
- `seed_layered_data.py` - Script Python pour créer les données de test
- `seed_layered_data.bat` - Script batch Windows pour créer les données de test

### 🧪 Scripts de Test
- `test_layered_api.py` - Script Python pour tester l'API
- `test_layered_api.bat` - Script batch Windows pour tester l'API

### ⚙️ Scripts de Setup
- `setup_layered.bat` - Script batch Windows pour le setup complet

## 🎯 Utilisation

### Depuis la Racine du Projet
```bash
# Setup complet
.\setup.bat

# Démarrer l'API
.\start.bat

# Créer les données de test
.\seed.bat

# Tester l'API
.\test.bat
```

### Depuis le Répertoire Scripts
```bash
# Démarrer l'API
.\start_layered.bat

# Créer les données de test
.\seed_layered_data.bat

# Tester l'API
.\test_layered_api.bat
```

## 📋 Prérequis

- Python 3.8+
- Environnement virtuel activé
- Dépendances installées (`pip install -r requirements.txt`)

## 🔧 Configuration

Les scripts utilisent automatiquement :
- L'environnement virtuel `venv/`
- La configuration de développement
- La base de données SQLite
- Le port 5000 pour l'API

## 📚 Documentation

- **API Documentation** : http://localhost:5000/docs/
- **Architecture** : Voir le README principal
- **Endpoints** : Documentation Swagger interactive

