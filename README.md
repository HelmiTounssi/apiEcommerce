# 🛒 Application E-commerce

Application e-commerce complète avec backend Flask et frontend Streamlit, utilisant une architecture en couches et l'authentification JWT.

## 🏗️ Architecture

### Backend (Flask)
- **Architecture :** Layered Architecture (Domain, Data, Service, Controller)
- **Base de données :** SQLite avec SQLAlchemy ORM
- **Authentification :** JWT (JSON Web Tokens)
- **API :** RESTful avec documentation Swagger
- **HATEOAS :** Liens hypermédia dans les réponses API

### Frontend (Streamlit)
- **Architecture :** MVP (Model-View-Presenter)
- **Interface :** Professionnelle avec sidebar d'authentification
- **Design :** Inspiré de Back Market

## 🚀 Démarrage Rapide

### Option 1 : Démarrage Complet (Recommandé)
```bash
.\start_all.bat
```
Lance automatiquement le backend et le frontend.

### Option 2 : Démarrage Séparé

#### Backend uniquement
```bash
.\start.bat
```
- Backend API : http://localhost:5000
- Documentation Swagger : http://localhost:5000/docs/

#### Frontend uniquement (Backend requis)
```bash
.\start_frontend.bat
```
- Interface : http://localhost:8501

## 🔐 Authentification

### Comptes de Test Disponibles
- **Admin :** `admin@ecommerce.com` / `admin123`
- **Client :** `client1@example.com` / `client123`

### Création de Nouveau Compte
- Utilisez un email **UNIQUE** (pas déjà utilisé)
- Exemple : `votre_nom@example.com`

## 📊 Entités

### Utilisateur
- Email unique
- Mot de passe haché
- Nom
- Rôle (client/admin)
- Date de création

### Produit
- Nom
- Description
- Catégorie
- Prix
- Quantité en stock
- Date de création

### Commande
- Utilisateur associé
- Date de commande
- Adresse de livraison
- Statut (en_attente, validée, expédiée, annulée)

### Ligne de Commande
- Commande associée
- Produit associé
- Quantité
- Prix unitaire au moment de la commande

## 🛠️ Technologies

### Backend
- **Flask** : Framework web
- **SQLAlchemy** : ORM
- **Flask-RESTX** : API REST avec Swagger
- **PyJWT** : Authentification JWT
- **Werkzeug** : Hachage des mots de passe

### Frontend
- **Streamlit** : Interface utilisateur
- **Requests** : Communication avec l'API
- **Pandas** : Manipulation des données
- **Plotly** : Visualisations

## 📁 Structure du Projet

```
apiEcommerce/
├── src/                    # Backend (Architecture en couches)
│   ├── domain/            # Entités métier
│   ├── data/              # Repositories et accès aux données
│   ├── service/           # Logique métier
│   ├── controller/        # API et DTOs
│   ├── config/            # Configuration
│   └── utils/             # Utilitaires
├── frontend/              # Frontend (Architecture MVP)
│   ├── models/            # Modèles de données
│   ├── services/          # Services API
│   ├── presenters/        # Logique de présentation
│   ├── views/             # Interfaces utilisateur
│   └── shared/            # Composants partagés
├── scripts/               # Scripts utilitaires
├── instance/              # Base de données SQLite
├── start.bat              # Démarrage backend
├── start_frontend.bat     # Démarrage frontend
├── start_all.bat          # Démarrage complet
└── requirements.txt       # Dépendances Python
```

## 🔧 Développement

### Installation des Dépendances
```bash
pip install -r requirements.txt
```

### Base de Données
La base de données SQLite est créée automatiquement au premier démarrage avec des données de test.

### Variables d'Environnement
- `JWT_SECRET_KEY` : Clé secrète pour JWT (défaut : 'jwt-secret-key-change-in-production')
- `JWT_ACCESS_TOKEN_EXPIRES` : Durée de vie du token (défaut : 3600 secondes)

## 📝 API Endpoints

### Authentification
- `POST /api/auth/register` : Inscription
- `POST /api/auth/login` : Connexion

### Utilisateurs
- `GET /api/utilisateurs/` : Liste des utilisateurs
- `GET /api/utilisateurs/{id}` : Détails d'un utilisateur
- `POST /api/utilisateurs/` : Création d'utilisateur
- `PUT /api/utilisateurs/{id}` : Modification d'utilisateur
- `DELETE /api/utilisateurs/{id}` : Suppression d'utilisateur

### Produits
- `GET /api/produits/` : Liste des produits
- `GET /api/produits/{id}` : Détails d'un produit
- `POST /api/produits/` : Création de produit
- `PUT /api/produits/{id}` : Modification de produit
- `DELETE /api/produits/{id}` : Suppression de produit

### Commandes
- `GET /api/commandes/` : Liste des commandes
- `GET /api/commandes/{id}` : Détails d'une commande
- `POST /api/commandes/` : Création de commande
- `PUT /api/commandes/{id}` : Modification de commande
- `DELETE /api/commandes/{id}` : Suppression de commande

## 🎯 Fonctionnalités

### Pour les Clients
- Création de compte et connexion
- Parcours du catalogue produits
- Passage de commandes
- Suivi des commandes

### Pour les Administrateurs
- Gestion du catalogue produits
- Suivi et modification des commandes
- Gestion des utilisateurs

## 🚨 Résolution de Problèmes

### Erreur 400 (Inscription)
- **Cause :** Email déjà utilisé
- **Solution :** Utilisez un email unique

### Erreur 401 (Connexion)
- **Cause :** Mauvais identifiants
- **Solution :** Vérifiez email et mot de passe

### Port déjà utilisé
- **Solution :** Fermez les autres instances ou utilisez un autre port

## 📞 Support

Pour toute question ou problème, vérifiez :
1. Que le backend est démarré (http://localhost:5000)
2. Que l'environnement virtuel est activé
3. Que toutes les dépendances sont installées
4. Les logs dans la console pour plus de détails