#!/bin/bash

# Script pour générer des certificats SSL auto-signés pour le développement

echo "🔐 Génération des certificats SSL pour le développement..."

# Créer le répertoire ssl s'il n'existe pas
mkdir -p ssl

# Générer la clé privée
openssl genrsa -out ssl/ecommerce.key 2048

# Générer le certificat auto-signé
openssl req -new -x509 -key ssl/ecommerce.key -out ssl/ecommerce.crt -days 365 -subj "/C=FR/ST=France/L=Paris/O=E-commerce/OU=IT/CN=localhost"

# Générer un certificat pour les domaines locaux
openssl req -new -x509 -key ssl/ecommerce.key -out ssl/ecommerce.crt -days 365 -subj "/C=FR/ST=France/L=Paris/O=E-commerce/OU=IT/CN=localhost" -addext "subjectAltName=DNS:localhost,DNS:127.0.0.1,IP:127.0.0.1"

echo "✅ Certificats SSL générés :"
echo "   - ssl/ecommerce.key (clé privée)"
echo "   - ssl/ecommerce.crt (certificat)"
echo ""
echo "⚠️  Ces certificats sont auto-signés et ne sont pas sécurisés pour la production !"
echo "   Votre navigateur affichera un avertissement de sécurité."
echo "   Cliquez sur 'Avancé' puis 'Continuer vers localhost' pour accéder au site."
