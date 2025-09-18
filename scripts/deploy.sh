#!/bin/bash

echo "🚀 Déploiement de l'application E-commerce avec Docker"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    print_error "Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

# Vérifier que Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

print_status "Arrêt des conteneurs existants..."
docker-compose down

print_status "Nettoyage des images orphelines..."
docker system prune -f

print_status "Construction et démarrage des nouveaux conteneurs..."
docker-compose up --build -d

# Attendre que les services soient prêts
print_status "Attente du démarrage des services..."
sleep 30

# Vérifier le statut des services
print_status "Vérification du statut des services..."
docker-compose ps

# Vérifier la santé des services
print_status "Vérification de la santé des services..."

# Backend health check
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    print_success "Backend est en ligne et fonctionnel"
else
    print_warning "Backend n'est pas encore prêt, attente supplémentaire..."
    sleep 10
    if curl -f http://localhost:5000/health > /dev/null 2>&1; then
        print_success "Backend est maintenant en ligne"
    else
        print_error "Backend ne répond pas"
    fi
fi

# Frontend health check
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    print_success "Frontend est en ligne et fonctionnel"
else
    print_warning "Frontend n'est pas encore prêt, attente supplémentaire..."
    sleep 10
    if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
        print_success "Frontend est maintenant en ligne"
    else
        print_error "Frontend ne répond pas"
    fi
fi

# Nginx health check
if curl -f http://localhost/health > /dev/null 2>&1; then
    print_success "Nginx est en ligne et fonctionnel"
else
    print_warning "Nginx n'est pas encore prêt"
fi

print_success "Déploiement terminé!"
echo ""
echo "🌐 Accès aux services:"
echo "   Frontend: http://localhost:8501"
echo "   Backend: http://localhost:5000"
echo "   API Docs: http://localhost:5000/docs/"
echo "   Nginx: http://localhost"
echo ""
echo "🔑 Comptes de test:"
echo "   Admin: admin@ecommerce.com / admin123"
echo "   Client: client1@example.com / client123"
echo ""
echo "📊 Commandes utiles:"
echo "   Voir les logs: docker-compose logs -f"
echo "   Arrêter: docker-compose down"
echo "   Redémarrer: docker-compose restart"
echo "   Statut: docker-compose ps"
