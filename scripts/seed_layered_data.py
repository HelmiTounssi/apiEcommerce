"""
Script pour peupler la base de données avec des données de test
"""

import sys
import os
from datetime import datetime

# Ajouter le répertoire src au path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.app import create_app
from src.data.database.db import db
from src.domain.models.utilisateur import Utilisateur
from src.domain.models.produit import Produit
from src.domain.models.commande import Commande
from src.domain.models.ligne_commande import LigneCommande


def create_test_users():
    """Crée des utilisateurs de test"""
    print("👥 Création des utilisateurs de test...")
    
    # Vérifier si des utilisateurs existent déjà
    if Utilisateur.query.first():
        print("   Utilisateurs déjà présents, suppression...")
        Utilisateur.query.delete()
        db.session.commit()
    
    # Créer des utilisateurs
    users_data = [
        {
            "email": "admin@ecommerce.com",
            "mot_de_passe": "admin123",
            "nom": "Administrateur",
            "role": "admin"
        },
        {
            "email": "client1@example.com",
            "mot_de_passe": "client123",
            "nom": "Jean Dupont",
            "role": "client"
        },
        {
            "email": "client2@example.com",
            "mot_de_passe": "client123",
            "nom": "Marie Martin",
            "role": "client"
        },
        {
            "email": "client3@example.com",
            "mot_de_passe": "client123",
            "nom": "Pierre Durand",
            "role": "client"
        }
    ]
    
    for user_data in users_data:
        user = Utilisateur(
            email=user_data["email"],
            mot_de_passe=user_data["mot_de_passe"],
            nom=user_data["nom"],
            role=user_data["role"]
        )
        db.session.add(user)
        print(f"   ✅ Utilisateur créé: {user_data['nom']} ({user_data['email']}) - {user_data['role']}")
    
    db.session.commit()
    print(f"   📊 {len(users_data)} utilisateurs créés")


def create_test_products():
    """Crée des produits de test"""
    print("\n📦 Création des produits de test...")
    
    # Vérifier si des produits existent déjà
    if Produit.query.first():
        print("   Produits déjà présents, suppression...")
        Produit.query.delete()
        db.session.commit()
    
    # Créer des produits
    products_data = [
        {
            "nom": "iPhone 13 Pro 128Go - Reconditionné",
            "description": "iPhone 13 Pro en excellent état, reconditionné par des professionnels. Garantie 12 mois.",
            "categorie": "Smartphones",
            "prix": 509.00,
            "quantite_stock": 15
        },
        {
            "nom": "MacBook Air 13\" M2 256Go - Reconditionné",
            "description": "MacBook Air avec puce M2, reconditionné. Performance exceptionnelle et autonomie longue durée.",
            "categorie": "Ordinateurs",
            "prix": 855.62,
            "quantite_stock": 8
        },
        {
            "nom": "iPad Air 5 64Go - Reconditionné",
            "description": "iPad Air 5ème génération, reconditionné. Parfait pour le travail et les loisirs.",
            "categorie": "Tablettes",
            "prix": 399.00,
            "quantite_stock": 12
        },
        {
            "nom": "Samsung Galaxy S22 128Go - Reconditionné",
            "description": "Samsung Galaxy S22 en très bon état, reconditionné. Appareil photo professionnel.",
            "categorie": "Smartphones",
            "prix": 299.00,
            "quantite_stock": 20
        },
        {
            "nom": "AirPods Pro 2ème génération - Reconditionné",
            "description": "AirPods Pro avec réduction de bruit active, reconditionnés. Son exceptionnel.",
            "categorie": "Audio",
            "prix": 149.00,
            "quantite_stock": 25
        },
        {
            "nom": "MacBook Pro 13\" M2 256Go - Reconditionné",
            "description": "MacBook Pro avec puce M2, reconditionné. Performance professionnelle.",
            "categorie": "Ordinateurs",
            "prix": 838.00,
            "quantite_stock": 5
        }
    ]
    
    for product_data in products_data:
        product = Produit(
            nom=product_data["nom"],
            description=product_data["description"],
            categorie=product_data["categorie"],
            prix=product_data["prix"],
            quantite_stock=product_data["quantite_stock"]
        )
        db.session.add(product)
        print(f"   ✅ Produit créé: {product_data['nom']} - €{product_data['prix']}")
    
    db.session.commit()
    print(f"   📊 {len(products_data)} produits créés")


def create_test_orders():
    """Crée des commandes de test"""
    print("\n🛒 Création des commandes de test...")
    
    # Vérifier si des commandes existent déjà
    if Commande.query.first():
        print("   Commandes déjà présentes, suppression...")
        Commande.query.delete()
        db.session.commit()
    
    # Récupérer les utilisateurs et produits
    users = Utilisateur.query.filter_by(role='client').all()
    products = Produit.query.all()
    
    if not users or not products:
        print("   ❌ Pas assez d'utilisateurs ou de produits pour créer des commandes")
        return
    
    # Créer des commandes
    orders_data = [
        {
            "utilisateur": users[0],
            "adresse_livraison": "123 Rue de la Paix, 75001 Paris",
            "statut": "validée",
            "lignes": [
                {"produit": products[0], "quantite": 1, "prix_unitaire": products[0].prix},
                {"produit": products[4], "quantite": 1, "prix_unitaire": products[4].prix}
            ]
        },
        {
            "utilisateur": users[1],
            "adresse_livraison": "456 Avenue des Champs, 75008 Paris",
            "statut": "en_attente",
            "lignes": [
                {"produit": products[1], "quantite": 1, "prix_unitaire": products[1].prix}
            ]
        },
        {
            "utilisateur": users[2],
            "adresse_livraison": "789 Boulevard Saint-Germain, 75006 Paris",
            "statut": "expédiée",
            "lignes": [
                {"produit": products[2], "quantite": 2, "prix_unitaire": products[2].prix},
                {"produit": products[3], "quantite": 1, "prix_unitaire": products[3].prix}
            ]
        }
    ]
    
    for order_data in orders_data:
        # Créer la commande
        commande = Commande(
            utilisateur_id=order_data["utilisateur"].id,
            adresse_livraison=order_data["adresse_livraison"],
            statut=order_data["statut"]
        )
        db.session.add(commande)
        db.session.flush()  # Pour obtenir l'ID de la commande
        
        # Créer les lignes de commande
        for ligne_data in order_data["lignes"]:
            ligne = LigneCommande(
                commande_id=commande.id,
                produit_id=ligne_data["produit"].id,
                quantite=ligne_data["quantite"],
                prix_unitaire=ligne_data["prix_unitaire"]
            )
            db.session.add(ligne)
        
        print(f"   ✅ Commande créée: {order_data['utilisateur'].nom} - {order_data['statut']}")
    
    db.session.commit()
    print(f"   📊 {len(orders_data)} commandes créées")


def main():
    """Fonction principale"""
    print("🌱 Peuplement de la base de données avec des données de test")
    print("=" * 60)
    
    # Créer l'application Flask
    app = create_app()
    
    with app.app_context():
        # Créer les tables si elles n'existent pas
        db.create_all()
        print("✅ Tables de base de données créées/vérifiées")
        
        # Créer les données de test
        create_test_users()
        create_test_products()
        create_test_orders()
        
        print("\n" + "=" * 60)
        print("✅ Base de données peuplée avec succès!")
        print("\n📋 Données créées:")
        print(f"   👥 Utilisateurs: {Utilisateur.query.count()}")
        print(f"   📦 Produits: {Produit.query.count()}")
        print(f"   🛒 Commandes: {Commande.query.count()}")
        print(f"   📝 Lignes de commande: {LigneCommande.query.count()}")
        
        print("\n🔐 Comptes de test créés:")
        print("   👨‍💼 Admin: admin@ecommerce.com / admin123")
        print("   👤 Client 1: client1@example.com / client123")
        print("   👤 Client 2: client2@example.com / client123")
        print("   👤 Client 3: client3@example.com / client123")


if __name__ == "__main__":
    main()

