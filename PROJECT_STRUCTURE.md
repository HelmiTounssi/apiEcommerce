# 📁 Structure du Projet E-commerce

## 🎯 Vue d'ensemble
Application e-commerce complète avec backend Flask et frontend Streamlit, utilisant une architecture en couches et l'authentification JWT.

## 📂 Structure des Dossiers

```
apiEcommerce/
├── 📁 src/                    # Backend (Architecture en couches)
│   ├── 📁 domain/            # Entités métier et modèles
│   ├── 📁 data/              # Repositories et accès aux données
│   ├── 📁 service/           # Logique métier
│   ├── 📁 controller/        # API et DTOs
│   ├── 📁 config/            # Configuration
│   └── 📁 utils/             # Utilitaires
├── 📁 frontend/              # Frontend (Architecture MVP)
│   ├── 📁 models/            # Modèles de données
│   ├── 📁 services/          # Services API
│   ├── 📁 presenters/        # Logique de présentation
│   ├── 📁 views/             # Interfaces utilisateur
│   └── 📁 shared/            # Composants partagés
├── 📁 scripts/               # Scripts utilitaires
│   ├── 📄 seed_layered_data.py    # Données de test
│   └── 📄 seed_layered_data.bat   # Exécution des données
├── 📁 instance/              # Base de données SQLite
│   ├── 📄 ecommerce.db            # Base de données principale
│   └── 📄 ecommerce_dev.db        # Base de données de développement
├── 📄 start.bat              # Démarrage backend
├── 📄 start_frontend.bat     # Démarrage frontend
├── 📄 start_all.bat          # Démarrage complet
├── 📄 start.py               # Script de démarrage backend
├── 📄 requirements.txt       # Dépendances Python
└── 📄 README.md              # Documentation principale
```

## 🚀 Scripts de Démarrage

### 📄 start.bat
- **Fonction :** Démarrage du backend uniquement
- **URL :** http://localhost:5000
- **Documentation :** http://localhost:5000/docs/

### 📄 start_frontend.bat
- **Fonction :** Démarrage du frontend (backend requis)
- **URL :** http://localhost:8501
- **Prérequis :** Backend actif sur le port 5000

### 📄 start_all.bat
- **Fonction :** Démarrage complet (backend + frontend)
- **URLs :** 
  - Backend : http://localhost:5000
  - Frontend : http://localhost:8501

## 🛠️ Scripts Utilitaires

### 📄 scripts/seed_layered_data.py
- **Fonction :** Création des données de test
- **Exécution :** `python scripts/seed_layered_data.py`

### 📄 scripts/seed_layered_data.bat
- **Fonction :** Exécution des données de test
- **Exécution :** `.\scripts\seed_layered_data.bat`

## 🗄️ Base de Données

### 📄 instance/ecommerce.db
- **Type :** SQLite
- **Contenu :** Données de production
- **Création :** Automatique au premier démarrage

### 📄 instance/ecommerce_dev.db
- **Type :** SQLite
- **Contenu :** Données de développement
- **Création :** Automatique au premier démarrage

## 📋 Dépendances

### 📄 requirements.txt
- **Flask** : Framework web backend
- **SQLAlchemy** : ORM
- **Flask-RESTX** : API REST avec Swagger
- **PyJWT** : Authentification JWT
- **Streamlit** : Interface utilisateur frontend
- **Requests** : Communication API
- **Pandas** : Manipulation des données
- **Plotly** : Visualisations

## 🔐 Authentification

### Comptes de Test
- **Admin :** `admin@ecommerce.com` / `admin123`
- **Client :** `client1@example.com` / `client123`

### Fonctionnalités
- ✅ Inscription avec validation
- ✅ Connexion avec JWT
- ✅ Gestion des rôles (client/admin)
- ✅ Messages d'erreur ergonomiques
- ✅ Aide contextuelle intégrée

## 🌐 URLs d'Accès

- **Backend API :** http://localhost:5000
- **Documentation Swagger :** http://localhost:5000/docs/
- **Frontend Interface :** http://localhost:8501

## 📝 Documentation

- **README.md** : Documentation complète
- **PROJECT_STRUCTURE.md** : Structure du projet (ce fichier)
- **scripts/README.md** : Documentation des scripts

## 🎯 Fonctionnalités

### Backend
- ✅ Architecture en couches
- ✅ API REST avec Swagger
- ✅ Authentification JWT
- ✅ HATEOAS (liens hypermédia)
- ✅ Base de données SQLite

### Frontend
- ✅ Architecture MVP
- ✅ Interface professionnelle
- ✅ Authentification intégrée
- ✅ Messages d'erreur ergonomiques
- ✅ Aide contextuelle

## 🔧 Maintenance

### Nettoyage
- ✅ Fichiers de test supprimés
- ✅ Scripts de débogage supprimés
- ✅ Structure organisée et propre

### Développement
- ✅ Code formaté et lisible
- ✅ Documentation à jour
- ✅ Scripts de démarrage simplifiés
