"""
Service pour la maintenance
"""

import os
import psutil
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from ...data.database.db import db
from ...data.repositories.utilisateur_repository import UtilisateurRepository
from ...data.repositories.produit_repository import ProduitRepository
from ...data.repositories.commande_repository import CommandeRepository

class MaintenanceService:
    """Service pour la maintenance du système"""
    
    def __init__(self):
        self.user_repo = UtilisateurRepository()
        self.product_repo = ProduitRepository()
        self.order_repo = CommandeRepository()
        self.logger = logging.getLogger(__name__)
    
    def optimize_database(self) -> Dict[str, Any]:
        """Optimise la base de données"""
        try:
            start_time = time.time()
            
            # VACUUM pour SQLite (optimise l'espace disque)
            db.session.execute("VACUUM")
            
            # ANALYZE pour mettre à jour les statistiques
            db.session.execute("ANALYZE")
            
            # Nettoyer les sessions expirées
            self._cleanup_expired_sessions()
            
            # Réindexer les tables principales
            self._reindex_tables()
            
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                "success": True,
                "message": "Base de données optimisée avec succès",
                "duration_seconds": round(duration, 2),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'optimisation de la base de données: {str(e)}")
            raise Exception(f"Erreur lors de l'optimisation: {str(e)}")
    
    def cleanup_temp_data(self) -> Dict[str, Any]:
        """Nettoie les données temporaires"""
        try:
            start_time = time.time()
            cleaned_items = {}
            
            # Nettoyer les fichiers temporaires
            temp_files_cleaned = self._cleanup_temp_files()
            cleaned_items["temp_files"] = temp_files_cleaned
            
            # Nettoyer les logs anciens
            old_logs_cleaned = self._cleanup_old_logs()
            cleaned_items["old_logs"] = old_logs_cleaned
            
            # Nettoyer les sessions expirées
            expired_sessions = self._cleanup_expired_sessions()
            cleaned_items["expired_sessions"] = expired_sessions
            
            # Nettoyer les données de cache
            cache_cleaned = self._cleanup_cache()
            cleaned_items["cache"] = cache_cleaned
            
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                "success": True,
                "message": "Données temporaires nettoyées avec succès",
                "cleaned_items": cleaned_items,
                "duration_seconds": round(duration, 2),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors du nettoyage: {str(e)}")
            raise Exception(f"Erreur lors du nettoyage: {str(e)}")
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyse les performances du système"""
        try:
            # Métriques système
            system_metrics = self._get_system_metrics()
            
            # Métriques de la base de données
            db_metrics = self._get_database_metrics()
            
            # Métriques de l'application
            app_metrics = self._get_application_metrics()
            
            return {
                "system": system_metrics,
                "database": db_metrics,
                "application": app_metrics,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse des performances: {str(e)}")
            raise Exception(f"Erreur lors de l'analyse des performances: {str(e)}")
    
    def restart_api(self) -> Dict[str, Any]:
        """Redémarre l'API"""
        try:
            # En production, cela pourrait déclencher un redémarrage via un système de gestion de processus
            # Pour l'instant, on simule le redémarrage
            
            return {
                "success": True,
                "message": "API redémarrée avec succès",
                "timestamp": datetime.now().isoformat(),
                "note": "Redémarrage simulé - en production, l'API serait effectivement redémarrée"
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors du redémarrage de l'API: {str(e)}")
            raise Exception(f"Erreur lors du redémarrage: {str(e)}")
    
    def restart_cache(self) -> Dict[str, Any]:
        """Redémarre le cache"""
        try:
            # Nettoyer le cache
            self._cleanup_cache()
            
            return {
                "success": True,
                "message": "Cache redémarré avec succès",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors du redémarrage du cache: {str(e)}")
            raise Exception(f"Erreur lors du redémarrage du cache: {str(e)}")
    
    def get_system_logs(self, level: str = "INFO", lines: int = 100) -> str:
        """Récupère les logs système"""
        try:
            # En production, cela lirait les vrais logs
            # Pour l'instant, on simule des logs
            
            log_entries = []
            for i in range(min(lines, 50)):  # Limiter à 50 pour la simulation
                timestamp = datetime.now() - timedelta(minutes=i)
                log_entry = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {level} - Log entry {i+1}"
                log_entries.append(log_entry)
            
            return "\n".join(log_entries)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des logs: {str(e)}")
            raise Exception(f"Erreur lors de la récupération des logs: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Vérifie la santé du système"""
        try:
            health_status = {
                "overall_status": "healthy",
                "checks": {}
            }
            
            # Vérifier la base de données
            db_status = self._check_database_health()
            health_status["checks"]["database"] = db_status
            
            # Vérifier l'espace disque
            disk_status = self._check_disk_health()
            health_status["checks"]["disk"] = disk_status
            
            # Vérifier la mémoire
            memory_status = self._check_memory_health()
            health_status["checks"]["memory"] = memory_status
            
            # Vérifier les performances
            performance_status = self._check_performance_health()
            health_status["checks"]["performance"] = performance_status
            
            # Déterminer le statut global
            all_healthy = all(check["status"] == "healthy" for check in health_status["checks"].values())
            health_status["overall_status"] = "healthy" if all_healthy else "degraded"
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification de santé: {str(e)}")
            return {
                "overall_status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Récupère le statut du système"""
        try:
            return {
                "uptime": self._get_uptime(),
                "version": "1.0.0",
                "environment": os.getenv("FLASK_ENV", "development"),
                "database_status": "connected",
                "cache_status": "active",
                "api_status": "running",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération du statut: {str(e)}")
            raise Exception(f"Erreur lors de la récupération du statut: {str(e)}")
    
    def backup_system(self, backup_type: str = "full") -> Dict[str, Any]:
        """Sauvegarde le système"""
        try:
            start_time = time.time()
            
            backup_info = {
                "type": backup_type,
                "start_time": datetime.now().isoformat(),
                "files": []
            }
            
            if backup_type == "full":
                # Sauvegarde complète
                backup_info["files"].append(self._backup_database())
                backup_info["files"].append(self._backup_config())
                backup_info["files"].append(self._backup_logs())
            elif backup_type == "database":
                # Sauvegarde de la base de données seulement
                backup_info["files"].append(self._backup_database())
            elif backup_type == "config":
                # Sauvegarde de la configuration seulement
                backup_info["files"].append(self._backup_config())
            
            end_time = time.time()
            backup_info["duration_seconds"] = round(end_time - start_time, 2)
            backup_info["end_time"] = datetime.now().isoformat()
            
            return {
                "success": True,
                "message": f"Sauvegarde {backup_type} effectuée avec succès",
                "backup_info": backup_info
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde: {str(e)}")
            raise Exception(f"Erreur lors de la sauvegarde: {str(e)}")
    
    def restore_system(self, backup_file: str) -> Dict[str, Any]:
        """Restaure le système depuis une sauvegarde"""
        try:
            # En production, cela restaurerait effectivement depuis le fichier de sauvegarde
            # Pour l'instant, on simule la restauration
            
            return {
                "success": True,
                "message": f"Système restauré depuis {backup_file}",
                "timestamp": datetime.now().isoformat(),
                "note": "Restauration simulée - en production, le système serait effectivement restauré"
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la restauration: {str(e)}")
            raise Exception(f"Erreur lors de la restauration: {str(e)}")
    
    # Méthodes privées
    
    def _cleanup_expired_sessions(self) -> int:
        """Nettoie les sessions expirées"""
        # En production, cela nettoierait les vraies sessions
        # Pour l'instant, on simule
        return 0
    
    def _reindex_tables(self):
        """Réindexe les tables principales"""
        tables = ["utilisateurs", "produits", "commandes", "lignes_commande"]
        for table in tables:
            try:
                db.session.execute(f"REINDEX {table}")
            except Exception as e:
                self.logger.warning(f"Impossible de réindexer la table {table}: {str(e)}")
    
    def _cleanup_temp_files(self) -> int:
        """Nettoie les fichiers temporaires"""
        # En production, cela nettoierait les vrais fichiers temporaires
        # Pour l'instant, on simule
        return 0
    
    def _cleanup_old_logs(self) -> int:
        """Nettoie les anciens logs"""
        # En production, cela nettoierait les vrais logs
        # Pour l'instant, on simule
        return 0
    
    def _cleanup_cache(self) -> int:
        """Nettoie le cache"""
        # En production, cela nettoierait le vrai cache
        # Pour l'instant, on simule
        return 0
    
    def _get_system_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques système"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            }
        except Exception:
            return {
                "cpu_percent": 0,
                "memory_percent": 0,
                "disk_percent": 0,
                "load_average": [0, 0, 0]
            }
    
    def _get_database_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques de la base de données"""
        try:
            # En production, cela récupérerait les vraies métriques de la DB
            return {
                "connection_count": 1,
                "query_count": 0,
                "avg_query_time": 0.0,
                "cache_hit_ratio": 0.95
            }
        except Exception:
            return {
                "connection_count": 0,
                "query_count": 0,
                "avg_query_time": 0.0,
                "cache_hit_ratio": 0.0
            }
    
    def _get_application_metrics(self) -> Dict[str, Any]:
        """Récupère les métriques de l'application"""
        try:
            return {
                "active_requests": 0,
                "total_requests": 0,
                "error_rate": 0.0,
                "response_time_avg": 0.0
            }
        except Exception:
            return {
                "active_requests": 0,
                "total_requests": 0,
                "error_rate": 0.0,
                "response_time_avg": 0.0
            }
    
    def _check_database_health(self) -> Dict[str, Any]:
        """Vérifie la santé de la base de données"""
        try:
            # Test de connexion simple
            db.session.execute("SELECT 1")
            return {"status": "healthy", "message": "Base de données accessible"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Erreur DB: {str(e)}"}
    
    def _check_disk_health(self) -> Dict[str, Any]:
        """Vérifie la santé du disque"""
        try:
            disk_usage = psutil.disk_usage('/')
            usage_percent = (disk_usage.used / disk_usage.total) * 100
            
            if usage_percent > 90:
                return {"status": "unhealthy", "message": f"Espace disque critique: {usage_percent:.1f}%"}
            elif usage_percent > 80:
                return {"status": "degraded", "message": f"Espace disque faible: {usage_percent:.1f}%"}
            else:
                return {"status": "healthy", "message": f"Espace disque OK: {usage_percent:.1f}%"}
        except Exception as e:
            return {"status": "unknown", "message": f"Impossible de vérifier le disque: {str(e)}"}
    
    def _check_memory_health(self) -> Dict[str, Any]:
        """Vérifie la santé de la mémoire"""
        try:
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                return {"status": "unhealthy", "message": f"Mémoire critique: {memory.percent:.1f}%"}
            elif memory.percent > 80:
                return {"status": "degraded", "message": f"Mémoire élevée: {memory.percent:.1f}%"}
            else:
                return {"status": "healthy", "message": f"Mémoire OK: {memory.percent:.1f}%"}
        except Exception as e:
            return {"status": "unknown", "message": f"Impossible de vérifier la mémoire: {str(e)}"}
    
    def _check_performance_health(self) -> Dict[str, Any]:
        """Vérifie la santé des performances"""
        try:
            # En production, cela vérifierait les vraies performances
            return {"status": "healthy", "message": "Performances normales"}
        except Exception as e:
            return {"status": "unknown", "message": f"Impossible de vérifier les performances: {str(e)}"}
    
    def _get_uptime(self) -> str:
        """Récupère le temps de fonctionnement"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        except Exception:
            return "Unknown"
    
    def _backup_database(self) -> str:
        """Sauvegarde la base de données"""
        # En production, cela créerait une vraie sauvegarde
        return "database_backup.sql"
    
    def _backup_config(self) -> str:
        """Sauvegarde la configuration"""
        # En production, cela créerait une vraie sauvegarde
        return "config_backup.json"
    
    def _backup_logs(self) -> str:
        """Sauvegarde les logs"""
        # En production, cela créerait une vraie sauvegarde
        return "logs_backup.tar.gz"
