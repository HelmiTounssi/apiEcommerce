#!/bin/bash

echo "🔧 Maintenance de l'application E-commerce"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Fonction de sauvegarde de la base de données
backup_database() {
    print_status "Sauvegarde de la base de données PostgreSQL..."
    
    BACKUP_DIR="./backups"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/ecommerce_backup_$TIMESTAMP.sql"
    
    mkdir -p $BACKUP_DIR
    
    if docker-compose exec -T postgres pg_dump -U ecommerce_user -d ecommerce > $BACKUP_FILE; then
        print_success "Sauvegarde PostgreSQL créée: $BACKUP_FILE"
    else
        print_error "Erreur lors de la sauvegarde de la base de données PostgreSQL"
    fi
}

# Fonction de nettoyage des logs
cleanup_logs() {
    print_status "Nettoyage des logs anciens..."
    
    if docker-compose exec -T backend find logs/ -name '*.log' -mtime +7 -delete 2>/dev/null; then
        print_success "Logs anciens supprimés"
    else
        print_warning "Aucun log ancien à supprimer"
    fi
}

# Fonction d'optimisation de la base de données
optimize_database() {
    print_status "Optimisation de la base de données PostgreSQL..."
    
    if docker-compose exec -T postgres psql -U ecommerce_user -d ecommerce -c "
-- ANALYZE pour mettre à jour les statistiques
ANALYZE;

-- VACUUM pour optimiser l'espace disque
VACUUM ANALYZE;

-- REINDEX pour reconstruire les index
REINDEX DATABASE ecommerce;
"; then
        print_success "Base de données PostgreSQL optimisée"
    else
        print_error "Erreur lors de l'optimisation de la base de données PostgreSQL"
    fi
}

# Fonction de redémarrage des services
restart_services() {
    print_status "Redémarrage des services..."
    
    docker-compose restart
    
    print_status "Attente du redémarrage..."
    sleep 15
    
    print_success "Services redémarrés"
}

# Fonction d'affichage des statistiques
show_stats() {
    print_status "Statistiques du système..."
    
    echo ""
    echo "📊 Statistiques des conteneurs:"
    docker-compose ps
    
    echo ""
    echo "💾 Utilisation des ressources:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
    
    echo ""
    echo "🗄️ Taille des volumes:"
    docker system df
}

# Menu principal
case "${1:-all}" in
    "backup")
        backup_database
        ;;
    "cleanup")
        cleanup_logs
        ;;
    "optimize")
        optimize_database
        ;;
    "restart")
        restart_services
        ;;
    "stats")
        show_stats
        ;;
    "all")
        print_status "Exécution de toutes les tâches de maintenance..."
        backup_database
        cleanup_logs
        optimize_database
        restart_services
        show_stats
        ;;
    *)
        echo "Usage: $0 {backup|cleanup|optimize|restart|stats|all}"
        echo ""
        echo "  backup   - Sauvegarder la base de données"
        echo "  cleanup  - Nettoyer les logs anciens"
        echo "  optimize - Optimiser la base de données"
        echo "  restart  - Redémarrer les services"
        echo "  stats    - Afficher les statistiques"
        echo "  all      - Exécuter toutes les tâches (défaut)"
        exit 1
        ;;
esac

print_success "Maintenance terminée!"
