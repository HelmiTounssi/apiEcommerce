"""
Health Check Controller
"""
from flask import jsonify
from flask_restx import Namespace, Resource

health_ns = Namespace('health', description='Health check endpoints')

@health_ns.route('/')
class HealthCheck(Resource):
    @health_ns.doc('health_check')
    def get(self):
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'ecommerce-backend',
            'version': '2.0.0'
        }), 200

@health_ns.route('/ready')
class ReadinessCheck(Resource):
    @health_ns.doc('readiness_check')
    def get(self):
        """Readiness check endpoint"""
        try:
            # Vérifier la connexion à la base de données
            from src.data.database.db import db
            db.session.execute('SELECT 1')
            
            return jsonify({
                'status': 'ready',
                'service': 'ecommerce-backend',
                'database': 'connected'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'not ready',
                'service': 'ecommerce-backend',
                'error': str(e)
            }), 503

@health_ns.route('/live')
class LivenessCheck(Resource):
    @health_ns.doc('liveness_check')
    def get(self):
        """Liveness check endpoint"""
        return jsonify({
            'status': 'alive',
            'service': 'ecommerce-backend'
        }), 200
