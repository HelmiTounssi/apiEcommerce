"""
Service pour la configuration
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

class ConfigService:
    """Service pour la gestion de la configuration"""
    
    def __init__(self):
        self.config_file = "config.json"
        self.default_config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retourne la configuration par défaut"""
        return {
            "app_name": "E-commerce API",
            "debug_mode": False,
            "maintenance_mode": False,
            "database": {
                "type": "SQLite",
                "pool_size": 10,
                "timeout": 30
            },
            "api": {
                "timeout": 30,
                "max_requests_per_minute": 100,
                "cors_enabled": True,
                "rate_limiting": True
            },
            "security": {
                "jwt_expiration": 1,  # heures
                "password_min_length": 8,
                "password_require_special": True,
                "session_timeout": 3600  # secondes
            },
            "logging": {
                "level": "INFO",
                "file_enabled": True,
                "console_enabled": True,
                "max_file_size": "10MB",
                "backup_count": 5
            },
            "cache": {
                "enabled": True,
                "ttl": 300,  # secondes
                "max_size": 1000
            },
            "email": {
                "enabled": False,
                "smtp_server": "",
                "smtp_port": 587,
                "username": "",
                "password": ""
            },
            "backup": {
                "enabled": True,
                "frequency": "daily",
                "retention_days": 30,
                "auto_cleanup": True
            }
        }
    
    def get_current_config(self) -> Dict[str, Any]:
        """Récupère la configuration actuelle"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return config
            else:
                # Créer le fichier de configuration avec les valeurs par défaut
                self.save_config(self.default_config)
                return self.default_config
                
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la configuration: {str(e)}")
    
    def update_config(self, new_config: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour la configuration"""
        try:
            # Récupérer la configuration actuelle
            current_config = self.get_current_config()
            
            # Fusionner avec la nouvelle configuration
            updated_config = self._merge_config(current_config, new_config)
            
            # Ajouter le timestamp de mise à jour
            updated_config['last_updated'] = datetime.now().isoformat()
            
            # Sauvegarder
            self.save_config(updated_config)
            
            return updated_config
            
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de la configuration: {str(e)}")
    
    def _merge_config(self, current: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Fusionne deux configurations"""
        merged = current.copy()
        
        for key, value in new.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_config(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Sauvegarde la configuration dans un fichier"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
            
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde de la configuration: {str(e)}")
    
    def get_app_config(self) -> Dict[str, Any]:
        """Récupère la configuration de l'application"""
        try:
            config = self.get_current_config()
            return {
                "app_name": config.get("app_name", "E-commerce API"),
                "debug_mode": config.get("debug_mode", False),
                "maintenance_mode": config.get("maintenance_mode", False)
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la config app: {str(e)}")
    
    def update_app_config(self, app_config: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour la configuration de l'application"""
        try:
            current_config = self.get_current_config()
            
            # Mettre à jour les paramètres de l'app
            for key, value in app_config.items():
                if key in ["app_name", "debug_mode", "maintenance_mode"]:
                    current_config[key] = value
            
            return self.update_config(current_config)
            
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de la config app: {str(e)}")
    
    def get_database_config(self) -> Dict[str, Any]:
        """Récupère la configuration de la base de données"""
        try:
            config = self.get_current_config()
            return config.get("database", {})
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la config DB: {str(e)}")
    
    def update_database_config(self, db_config: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour la configuration de la base de données"""
        try:
            current_config = self.get_current_config()
            current_config["database"] = db_config
            
            return self.update_config(current_config)
            
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de la config DB: {str(e)}")
    
    def get_api_config(self) -> Dict[str, Any]:
        """Récupère la configuration de l'API"""
        try:
            config = self.get_current_config()
            return config.get("api", {})
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la config API: {str(e)}")
    
    def update_api_config(self, api_config: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour la configuration de l'API"""
        try:
            current_config = self.get_current_config()
            current_config["api"] = api_config
            
            return self.update_config(current_config)
            
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de la config API: {str(e)}")
    
    def get_security_config(self) -> Dict[str, Any]:
        """Récupère la configuration de sécurité"""
        try:
            config = self.get_current_config()
            return config.get("security", {})
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la config sécurité: {str(e)}")
    
    def update_security_config(self, security_config: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour la configuration de sécurité"""
        try:
            current_config = self.get_current_config()
            current_config["security"] = security_config
            
            return self.update_config(current_config)
            
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de la config sécurité: {str(e)}")
    
    def reset_to_default(self) -> Dict[str, Any]:
        """Réinitialise la configuration aux valeurs par défaut"""
        try:
            # Ajouter le timestamp de réinitialisation
            self.default_config['last_reset'] = datetime.now().isoformat()
            
            # Sauvegarder la configuration par défaut
            self.save_config(self.default_config)
            
            return self.default_config
            
        except Exception as e:
            raise Exception(f"Erreur lors de la réinitialisation: {str(e)}")
    
    def backup_config(self) -> Dict[str, Any]:
        """Sauvegarde la configuration actuelle"""
        try:
            config = self.get_current_config()
            backup_data = {
                "config": config,
                "backup_date": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            # Sauvegarder dans un fichier de backup
            backup_file = f"config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            return {
                "backup_file": backup_file,
                "backup_date": backup_data["backup_date"],
                "config": config
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde: {str(e)}")
    
    def restore_config(self, backup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Restaure une configuration sauvegardée"""
        try:
            if "config" not in backup_data:
                raise Exception("Données de sauvegarde invalides")
            
            config = backup_data["config"]
            config['restored_from'] = backup_data.get("backup_date", "unknown")
            config['restore_date'] = datetime.now().isoformat()
            
            # Sauvegarder la configuration restaurée
            self.save_config(config)
            
            return config
            
        except Exception as e:
            raise Exception(f"Erreur lors de la restauration: {str(e)}")
    
    def validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Valide une configuration"""
        try:
            errors = []
            warnings = []
            
            # Validation des paramètres obligatoires
            required_fields = ["app_name", "database", "api", "security"]
            for field in required_fields:
                if field not in config:
                    errors.append(f"Champ obligatoire manquant: {field}")
            
            # Validation de la configuration de la base de données
            if "database" in config:
                db_config = config["database"]
                if "pool_size" in db_config and db_config["pool_size"] < 1:
                    errors.append("La taille du pool de connexions doit être >= 1")
                if "pool_size" in db_config and db_config["pool_size"] > 100:
                    warnings.append("La taille du pool de connexions est élevée")
            
            # Validation de la configuration de l'API
            if "api" in config:
                api_config = config["api"]
                if "timeout" in api_config and api_config["timeout"] < 1:
                    errors.append("Le timeout API doit être >= 1 seconde")
                if "max_requests_per_minute" in api_config and api_config["max_requests_per_minute"] < 1:
                    errors.append("Le nombre max de requêtes par minute doit être >= 1")
            
            # Validation de la configuration de sécurité
            if "security" in config:
                security_config = config["security"]
                if "jwt_expiration" in security_config and security_config["jwt_expiration"] < 1:
                    errors.append("L'expiration JWT doit être >= 1 heure")
                if "password_min_length" in security_config and security_config["password_min_length"] < 6:
                    errors.append("La longueur minimale du mot de passe doit être >= 6")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la validation: {str(e)}")
    
    def get_config_history(self) -> List[Dict[str, Any]]:
        """Récupère l'historique des modifications de configuration"""
        try:
            # Cette fonctionnalité nécessiterait une base de données pour stocker l'historique
            # Pour l'instant, on retourne une liste vide
            return []
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de l'historique: {str(e)}")
    
    def export_config(self, format_type: str = "json") -> str:
        """Exporte la configuration dans un format spécifique"""
        try:
            config = self.get_current_config()
            
            if format_type == "json":
                return json.dumps(config, indent=2, ensure_ascii=False)
            elif format_type == "yaml":
                import yaml
                return yaml.dump(config, default_flow_style=False, allow_unicode=True)
            else:
                raise Exception(f"Format d'export non supporté: {format_type}")
                
        except Exception as e:
            raise Exception(f"Erreur lors de l'export: {str(e)}")
    
    def import_config(self, config_data: str, format_type: str = "json") -> Dict[str, Any]:
        """Importe une configuration depuis un format spécifique"""
        try:
            if format_type == "json":
                config = json.loads(config_data)
            elif format_type == "yaml":
                import yaml
                config = yaml.safe_load(config_data)
            else:
                raise Exception(f"Format d'import non supporté: {format_type}")
            
            # Valider la configuration
            validation = self.validate_config(config)
            if not validation["valid"]:
                raise Exception(f"Configuration invalide: {validation['errors']}")
            
            # Sauvegarder la configuration importée
            return self.update_config(config)
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'import: {str(e)}")
