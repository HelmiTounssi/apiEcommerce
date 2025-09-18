"""
Service pour les rapports
"""

import csv
import io
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from ...data.repositories.utilisateur_repository import UtilisateurRepository
from ...data.repositories.produit_repository import ProduitRepository
from ...data.repositories.commande_repository import CommandeRepository
from ...data.repositories.ligne_commande_repository import LigneCommandeRepository

class ReportsService:
    """Service pour la génération de rapports"""
    
    def __init__(self):
        self.user_repo = UtilisateurRepository()
        self.product_repo = ProduitRepository()
        self.order_repo = CommandeRepository()
        self.line_repo = LigneCommandeRepository()
    
    def generate_sales_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Génère le rapport des ventes"""
        try:
            # Parser les dates
            start_dt = self._parse_date(start_date) if start_date else datetime.now().date() - timedelta(days=30)
            end_dt = self._parse_date(end_date) if end_date else datetime.now().date()
            
            # Récupérer les données de ventes
            total_sales = self.order_repo.get_revenue_by_date_range(start_dt, end_dt) or 0.0
            total_orders = self.order_repo.count_by_date_range(start_dt, end_dt)
            average_order = total_sales / total_orders if total_orders > 0 else 0.0
            
            # Données de ventes par période
            sales_data = self.order_repo.get_revenue_by_date_range_chart(start_dt, end_dt)
            
            return {
                "total_sales": total_sales,
                "total_orders": total_orders,
                "average_order": average_order,
                "period": {
                    "start_date": start_dt.isoformat(),
                    "end_date": end_dt.isoformat()
                },
                "sales_data": sales_data
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du rapport ventes: {str(e)}")
    
    def generate_top_clients_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """Génère le rapport des top clients"""
        try:
            # Parser les dates
            start_dt = self._parse_date(start_date) if start_date else datetime.now().date() - timedelta(days=30)
            end_dt = self._parse_date(end_date) if end_date else datetime.now().date()
            
            # Récupérer les top clients
            top_clients = self.order_repo.get_top_clients(start_dt, end_dt, limit)
            
            return {
                "period": {
                    "start_date": start_dt.isoformat(),
                    "end_date": end_dt.isoformat()
                },
                "clients": top_clients
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du rapport top clients: {str(e)}")
    
    def generate_top_products_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """Génère le rapport des produits les plus vendus"""
        try:
            # Parser les dates
            start_dt = self._parse_date(start_date) if start_date else datetime.now().date() - timedelta(days=30)
            end_dt = self._parse_date(end_date) if end_date else datetime.now().date()
            
            # Récupérer les top produits
            top_products = self.line_repo.get_top_products_by_date_range(start_dt, end_dt, limit)
            
            return {
                "period": {
                    "start_date": start_dt.isoformat(),
                    "end_date": end_dt.isoformat()
                },
                "products": top_products
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du rapport top produits: {str(e)}")
    
    def generate_orders_analysis_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Génère l'analyse des commandes"""
        try:
            # Parser les dates
            start_dt = self._parse_date(start_date) if start_date else datetime.now().date() - timedelta(days=30)
            end_dt = self._parse_date(end_date) if end_date else datetime.now().date()
            
            # Analyse par statut
            status_analysis = self.order_repo.get_orders_by_status_in_range(start_dt, end_dt)
            
            # Analyse temporelle
            temporal_analysis = self.order_repo.get_orders_by_date_range(start_dt, end_dt)
            
            return {
                "period": {
                    "start_date": start_dt.isoformat(),
                    "end_date": end_dt.isoformat()
                },
                "status_analysis": status_analysis,
                "temporal_analysis": temporal_analysis
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération de l'analyse commandes: {str(e)}")
    
    def generate_performance_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Génère le rapport de performance"""
        try:
            # Parser les dates
            start_dt = self._parse_date(start_date) if start_date else datetime.now().date() - timedelta(days=30)
            end_dt = self._parse_date(end_date) if end_date else datetime.now().date()
            
            # Métriques de performance (simulées pour l'instant)
            avg_response_time = 150.0  # ms
            requests_per_minute = 45
            error_rate = 0.5  # %
            
            # Données de performance par période
            performance_data = self._generate_performance_data(start_dt, end_dt)
            
            return {
                "period": {
                    "start_date": start_dt.isoformat(),
                    "end_date": end_dt.isoformat()
                },
                "avg_response_time": avg_response_time,
                "requests_per_minute": requests_per_minute,
                "error_rate": error_rate,
                "performance_data": performance_data
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du rapport performance: {str(e)}")
    
    def export_report(self, report_type: str, format_type: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Any:
        """Exporte un rapport dans un format spécifique"""
        try:
            # Générer le rapport
            if report_type == "sales":
                report_data = self.generate_sales_report(start_date, end_date)
            elif report_type == "top_clients":
                report_data = self.generate_top_clients_report(start_date, end_date)
            elif report_type == "top_products":
                report_data = self.generate_top_products_report(start_date, end_date)
            elif report_type == "orders_analysis":
                report_data = self.generate_orders_analysis_report(start_date, end_date)
            elif report_type == "performance":
                report_data = self.generate_performance_report(start_date, end_date)
            else:
                raise Exception(f"Type de rapport non supporté: {report_type}")
            
            # Exporter dans le format demandé
            if format_type == "csv":
                return self._export_to_csv(report_data, report_type)
            elif format_type == "json":
                return report_data
            elif format_type == "pdf":
                return self._export_to_pdf(report_data, report_type)
            else:
                raise Exception(f"Format d'export non supporté: {format_type}")
                
        except Exception as e:
            raise Exception(f"Erreur lors de l'export: {str(e)}")
    
    def get_scheduled_reports(self) -> List[Dict[str, Any]]:
        """Récupère la liste des rapports programmés"""
        try:
            # En production, cela récupérerait les vrais rapports programmés depuis la base de données
            # Pour l'instant, on simule
            return [
                {
                    "id": 1,
                    "name": "Rapport Ventes Quotidien",
                    "type": "sales",
                    "schedule": "daily",
                    "time": "08:00",
                    "enabled": True,
                    "recipients": ["admin@example.com"]
                },
                {
                    "id": 2,
                    "name": "Rapport Performance Hebdomadaire",
                    "type": "performance",
                    "schedule": "weekly",
                    "day": "monday",
                    "time": "09:00",
                    "enabled": True,
                    "recipients": ["admin@example.com", "manager@example.com"]
                }
            ]
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des rapports programmés: {str(e)}")
    
    def create_scheduled_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un rapport programmé"""
        try:
            # En production, cela créerait un vrai rapport programmé dans la base de données
            # Pour l'instant, on simule
            
            scheduled_report = {
                "id": 999,  # ID simulé
                "name": report_data.get("name", "Nouveau Rapport"),
                "type": report_data.get("type", "sales"),
                "schedule": report_data.get("schedule", "daily"),
                "enabled": report_data.get("enabled", True),
                "created_at": datetime.now().isoformat()
            }
            
            return scheduled_report
            
        except Exception as e:
            raise Exception(f"Erreur lors de la création du rapport programmé: {str(e)}")
    
    def update_scheduled_report(self, report_id: int, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour un rapport programmé"""
        try:
            # En production, cela mettrait à jour le vrai rapport programmé
            # Pour l'instant, on simule
            
            updated_report = {
                "id": report_id,
                "name": report_data.get("name", "Rapport Modifié"),
                "type": report_data.get("type", "sales"),
                "schedule": report_data.get("schedule", "daily"),
                "enabled": report_data.get("enabled", True),
                "updated_at": datetime.now().isoformat()
            }
            
            return updated_report
            
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour du rapport programmé: {str(e)}")
    
    def delete_scheduled_report(self, report_id: int) -> Dict[str, Any]:
        """Supprime un rapport programmé"""
        try:
            # En production, cela supprimerait le vrai rapport programmé
            # Pour l'instant, on simule
            
            return {
                "id": report_id,
                "deleted": True,
                "deleted_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la suppression du rapport programmé: {str(e)}")
    
    # Méthodes privées
    
    def _parse_date(self, date_str: str) -> datetime.date:
        """Parse une chaîne de date"""
        try:
            return datetime.fromisoformat(date_str).date()
        except ValueError:
            raise Exception(f"Format de date invalide: {date_str}")
    
    def _export_to_csv(self, report_data: Dict[str, Any], report_type: str) -> str:
        """Exporte un rapport en CSV"""
        try:
            output = io.StringIO()
            writer = csv.writer(output)
            
            if report_type == "sales":
                # En-têtes
                writer.writerow(["Date", "Ventes", "Commandes", "Panier Moyen"])
                
                # Données
                for item in report_data.get("sales_data", []):
                    writer.writerow([
                        item.get("date", ""),
                        item.get("revenue", 0),
                        item.get("count", 0),
                        item.get("average", 0)
                    ])
            
            elif report_type == "top_clients":
                # En-têtes
                writer.writerow(["Client", "Email", "Commandes", "CA Total"])
                
                # Données
                for client in report_data.get("clients", []):
                    writer.writerow([
                        client.get("nom", ""),
                        client.get("email", ""),
                        client.get("order_count", 0),
                        client.get("total_spent", 0)
                    ])
            
            elif report_type == "top_products":
                # En-têtes
                writer.writerow(["Produit", "Quantité Vendue", "CA Généré"])
                
                # Données
                for product in report_data.get("products", []):
                    writer.writerow([
                        product.get("nom", ""),
                        product.get("quantity_sold", 0),
                        product.get("revenue", 0)
                    ])
            
            return output.getvalue()
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'export CSV: {str(e)}")
    
    def _export_to_pdf(self, report_data: Dict[str, Any], report_type: str) -> bytes:
        """Exporte un rapport en PDF"""
        try:
            # En production, cela utiliserait une bibliothèque comme ReportLab
            # Pour l'instant, on simule en retournant des données binaires
            pdf_content = f"PDF Report: {report_type}\nGenerated: {datetime.now()}\nData: {report_data}"
            return pdf_content.encode('utf-8')
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'export PDF: {str(e)}")
    
    def _generate_performance_data(self, start_date: datetime.date, end_date: datetime.date) -> List[Dict[str, Any]]:
        """Génère des données de performance simulées"""
        performance_data = []
        current_date = start_date
        
        while current_date <= end_date:
            performance_data.append({
                "date": current_date.isoformat(),
                "response_time": 150.0 + (current_date.day % 10) * 5,  # Simulation
                "requests_per_minute": 40 + (current_date.day % 20),  # Simulation
                "error_rate": 0.5 + (current_date.day % 5) * 0.1  # Simulation
            })
            current_date += timedelta(days=1)
        
        return performance_data
