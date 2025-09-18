"""
Contrôleur pour les rapports
"""

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from ...utils.auth_decorators import token_required, admin_required
from ...service.impl.reports_service import ReportsService

# Créer le namespace pour les rapports
reports_ns = Namespace('reports', description='Rapports du système')

# Modèles de données pour la documentation Swagger
sales_report_model = reports_ns.model('SalesReport', {
    'total_sales': fields.Float(description='Total des ventes'),
    'total_orders': fields.Integer(description='Nombre total de commandes'),
    'average_order': fields.Float(description='Panier moyen'),
    'sales_data': fields.List(fields.Raw, description='Données de ventes par période')
})

top_clients_model = reports_ns.model('TopClients', {
    'clients': fields.List(fields.Raw, description='Liste des top clients')
})

top_products_model = reports_ns.model('TopProducts', {
    'products': fields.List(fields.Raw, description='Liste des produits les plus vendus')
})

orders_analysis_model = reports_ns.model('OrdersAnalysis', {
    'status_analysis': fields.List(fields.Raw, description='Analyse par statut'),
    'temporal_analysis': fields.List(fields.Raw, description='Analyse temporelle')
})

performance_report_model = reports_ns.model('PerformanceReport', {
    'avg_response_time': fields.Float(description='Temps de réponse moyen'),
    'requests_per_minute': fields.Integer(description='Requêtes par minute'),
    'error_rate': fields.Float(description='Taux d\'erreur'),
    'performance_data': fields.List(fields.Raw, description='Données de performance')
})

@reports_ns.route('/generate')
class GenerateReportResource(Resource):
    """Ressource pour générer des rapports"""
    
    @reports_ns.doc('generate_report')
    @token_required
    def get(self):
        """Génère un rapport selon le type demandé"""
        try:
            report_type = request.args.get('type')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            if not report_type:
                return {
                    'success': False,
                    'message': 'Type de rapport manquant'
                }, 400
            
            reports_service = ReportsService()
            
            if report_type == 'sales':
                report_data = reports_service.generate_sales_report(start_date, end_date)
            elif report_type == 'top_clients':
                report_data = reports_service.generate_top_clients_report(start_date, end_date)
            elif report_type == 'top_products':
                report_data = reports_service.generate_top_products_report(start_date, end_date)
            elif report_type == 'orders_analysis':
                report_data = reports_service.generate_orders_analysis_report(start_date, end_date)
            elif report_type == 'performance':
                report_data = reports_service.generate_performance_report(start_date, end_date)
            else:
                return {
                    'success': False,
                    'message': 'Type de rapport non supporté'
                }, 400
            
            return {
                'success': True,
                'data': report_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la génération du rapport: {str(e)}'
            }, 500

@reports_ns.route('/sales')
class SalesReportResource(Resource):
    """Ressource pour le rapport des ventes"""
    
    @reports_ns.doc('generate_sales_report')
    @reports_ns.marshal_with(sales_report_model)
    @token_required
    def get(self):
        """Génère le rapport des ventes"""
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            reports_service = ReportsService()
            report_data = reports_service.generate_sales_report(start_date, end_date)
            
            return {
                'success': True,
                'data': report_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la génération du rapport ventes: {str(e)}'
            }, 500

@reports_ns.route('/top-clients')
class TopClientsReportResource(Resource):
    """Ressource pour le rapport des top clients"""
    
    @reports_ns.doc('generate_top_clients_report')
    @reports_ns.marshal_with(top_clients_model)
    @token_required
    def get(self):
        """Génère le rapport des top clients"""
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            limit = request.args.get('limit', 10, type=int)
            
            reports_service = ReportsService()
            report_data = reports_service.generate_top_clients_report(start_date, end_date, limit)
            
            return {
                'success': True,
                'data': report_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la génération du rapport top clients: {str(e)}'
            }, 500

@reports_ns.route('/top-products')
class TopProductsReportResource(Resource):
    """Ressource pour le rapport des produits les plus vendus"""
    
    @reports_ns.doc('generate_top_products_report')
    @reports_ns.marshal_with(top_products_model)
    @token_required
    def get(self):
        """Génère le rapport des produits les plus vendus"""
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            limit = request.args.get('limit', 10, type=int)
            
            reports_service = ReportsService()
            report_data = reports_service.generate_top_products_report(start_date, end_date, limit)
            
            return {
                'success': True,
                'data': report_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la génération du rapport top produits: {str(e)}'
            }, 500

@reports_ns.route('/orders-analysis')
class OrdersAnalysisReportResource(Resource):
    """Ressource pour l'analyse des commandes"""
    
    @reports_ns.doc('generate_orders_analysis_report')
    @reports_ns.marshal_with(orders_analysis_model)
    @token_required
    def get(self):
        """Génère l'analyse des commandes"""
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            reports_service = ReportsService()
            report_data = reports_service.generate_orders_analysis_report(start_date, end_date)
            
            return {
                'success': True,
                'data': report_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la génération de l\'analyse commandes: {str(e)}'
            }, 500

@reports_ns.route('/performance')
class PerformanceReportResource(Resource):
    """Ressource pour le rapport de performance"""
    
    @reports_ns.doc('generate_performance_report')
    @reports_ns.marshal_with(performance_report_model)
    @token_required
    def get(self):
        """Génère le rapport de performance"""
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            reports_service = ReportsService()
            report_data = reports_service.generate_performance_report(start_date, end_date)
            
            return {
                'success': True,
                'data': report_data
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la génération du rapport performance: {str(e)}'
            }, 500

@reports_ns.route('/export')
class ExportReportResource(Resource):
    """Ressource pour exporter des rapports"""
    
    @reports_ns.doc('export_report')
    @token_required
    def get(self):
        """Exporte un rapport dans un format spécifique"""
        try:
            report_type = request.args.get('type')
            format_type = request.args.get('format', 'json')  # json, csv, pdf
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            if not report_type:
                return {
                    'success': False,
                    'message': 'Type de rapport manquant'
                }, 400
            
            reports_service = ReportsService()
            export_data = reports_service.export_report(report_type, format_type, start_date, end_date)
            
            if format_type == 'csv':
                return export_data, 200, {
                    'Content-Type': 'text/csv',
                    'Content-Disposition': f'attachment; filename={report_type}_report.csv'
                }
            elif format_type == 'pdf':
                return export_data, 200, {
                    'Content-Type': 'application/pdf',
                    'Content-Disposition': f'attachment; filename={report_type}_report.pdf'
                }
            else:  # json
                return {
                    'success': True,
                    'data': export_data
                }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de l\'export: {str(e)}'
            }, 500

@reports_ns.route('/scheduled')
class ScheduledReportsResource(Resource):
    """Ressource pour les rapports programmés"""
    
    @reports_ns.doc('get_scheduled_reports')
    @token_required
    def get(self):
        """Récupère la liste des rapports programmés"""
        try:
            reports_service = ReportsService()
            scheduled_reports = reports_service.get_scheduled_reports()
            
            return {
                'success': True,
                'data': scheduled_reports
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la récupération des rapports programmés: {str(e)}'
            }, 500
    
    @reports_ns.doc('create_scheduled_report')
    @admin_required
    def post(self):
        """Crée un rapport programmé"""
        try:
            report_data = request.get_json()
            
            if not report_data:
                return {
                    'success': False,
                    'message': 'Données du rapport manquantes'
                }, 400
            
            reports_service = ReportsService()
            scheduled_report = reports_service.create_scheduled_report(report_data)
            
            return {
                'success': True,
                'message': 'Rapport programmé créé avec succès',
                'data': scheduled_report
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la création du rapport programmé: {str(e)}'
            }, 500

@reports_ns.route('/scheduled/<int:report_id>')
class ScheduledReportResource(Resource):
    """Ressource pour un rapport programmé spécifique"""
    
    @reports_ns.doc('update_scheduled_report')
    @admin_required
    def put(self, report_id):
        """Met à jour un rapport programmé"""
        try:
            report_data = request.get_json()
            
            if not report_data:
                return {
                    'success': False,
                    'message': 'Données du rapport manquantes'
                }, 400
            
            reports_service = ReportsService()
            updated_report = reports_service.update_scheduled_report(report_id, report_data)
            
            return {
                'success': True,
                'message': 'Rapport programmé mis à jour avec succès',
                'data': updated_report
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la mise à jour du rapport programmé: {str(e)}'
            }, 500
    
    @reports_ns.doc('delete_scheduled_report')
    @admin_required
    def delete(self, report_id):
        """Supprime un rapport programmé"""
        try:
            reports_service = ReportsService()
            result = reports_service.delete_scheduled_report(report_id)
            
            return {
                'success': True,
                'message': 'Rapport programmé supprimé avec succès',
                'data': result
            }, 200
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur lors de la suppression du rapport programmé: {str(e)}'
            }, 500
