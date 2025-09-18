"""
Contrôleur API pour le panier
"""

import logging
from flask import request
from flask_restx import Resource, Namespace, fields
from ...service.impl.panier_service import PanierService
from ...controller.dto.panier_dto import AjouterAuPanierDTO, ModifierQuantiteDTO, SupprimerDuPanierDTO
from ...utils.auth_decorators import token_required, optional_auth, get_current_user
from ...utils.logging_config import get_logger, log_business_operation, log_database_operation
from ...utils.request_logging import log_request_response, log_user_action

# Configuration du logger
logger = get_logger(__name__)

# Namespace pour le panier
panier_ns = Namespace('panier', description='Opérations sur le panier')

# Modèles Swagger
panier_item_model = panier_ns.model('PanierItem', {
    'id': fields.Integer(readonly=True, description='ID de l\'item'),
    'panier_id': fields.Integer(description='ID du panier'),
    'produit_id': fields.Integer(description='ID du produit'),
    'quantite': fields.Integer(description='Quantité'),
    'prix_unitaire': fields.Float(description='Prix unitaire'),
    'sous_total': fields.Float(description='Sous-total'),
    'produit': fields.String(description='Informations du produit')
})

panier_model = panier_ns.model('Panier', {
    'id': fields.Integer(readonly=True, description='ID du panier'),
    'utilisateur_id': fields.Integer(description='ID de l\'utilisateur'),
    'session_id': fields.String(description='ID de session'),
    'date_creation': fields.DateTime(readonly=True, description='Date de création'),
    'date_modification': fields.DateTime(readonly=True, description='Date de modification'),
    'statut': fields.String(description='Statut du panier'),
    'total': fields.Float(description='Total du panier'),
    'nombre_items': fields.Integer(description='Nombre d\'items'),
    'items': fields.List(fields.Nested(panier_item_model), description='Items du panier')
})

ajouter_au_panier_model = panier_ns.model('AjouterAuPanier', {
    'produit_id': fields.Integer(required=True, description='ID du produit'),
    'quantite': fields.Integer(description='Quantité à ajouter', default=1)
})

modifier_quantite_model = panier_ns.model('ModifierQuantite', {
    'produit_id': fields.Integer(required=True, description='ID du produit'),
    'quantite': fields.Integer(required=True, description='Nouvelle quantité')
})

supprimer_du_panier_model = panier_ns.model('SupprimerDuPanier', {
    'produit_id': fields.Integer(required=True, description='ID du produit')
})

panier_resume_model = panier_ns.model('PanierResume', {
    'nombre_items': fields.Integer(description='Nombre d\'items'),
    'total': fields.Float(description='Total du panier'),
    'items': fields.List(fields.Raw, description='Items du panier')
})

# Service
panier_service = PanierService()


@panier_ns.route('/')
class PanierResource(Resource):
    @panier_ns.doc('get_panier')
    @panier_ns.marshal_with(panier_model)
    @optional_auth
    @log_request_response
    def get(self):
        """Récupère le panier de l'utilisateur ou de la session"""
        try:
            user = get_current_user()
            session_id = request.headers.get('X-Session-ID', 'default')
            
            logger.info(f"🔍 Récupération du panier | User: {user['id'] if user else 'Anonymous'} | Session: {session_id}")
            
            if user:
                # Utilisateur connecté
                log_business_operation('PanierService', 'get_panier_utilisateur', user_id=user['id'])
                panier = panier_service.get_panier_utilisateur(user['id'])
                
                if panier:
                    logger.info(f"✅ Panier trouvé pour utilisateur {user['id']} | Items: {len(panier.items) if panier.items else 0}")
                    log_user_action('get_cart', user['id'], cart_id=panier.id, items_count=len(panier.items) if panier.items else 0)
                    return panier.to_dict()
                else:
                    logger.info(f"📭 Panier vide pour utilisateur {user['id']}")
                    return {'message': 'Panier vide'}, 200
            else:
                # Utilisateur non connecté - utiliser session
                log_business_operation('PanierService', 'get_panier_session', data={'session_id': session_id})
                panier = panier_service.get_panier_session(session_id)
                
                if panier:
                    logger.info(f"✅ Panier trouvé pour session {session_id} | Items: {len(panier.items) if panier.items else 0}")
                    log_user_action('get_cart_anonymous', None, session_id=session_id, cart_id=panier.id, items_count=len(panier.items) if panier.items else 0)
                    return panier.to_dict()
                else:
                    logger.info(f"📭 Panier vide pour session {session_id}")
                    return {'message': 'Panier vide'}, 200
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération du panier: {e}")
            log_business_operation('PanierService', 'get_panier', error=str(e))
            return {'message': 'Erreur lors de la récupération du panier'}, 500


@panier_ns.route('/resume')
class PanierResumeResource(Resource):
    @panier_ns.doc('get_panier_resume')
    @panier_ns.marshal_with(panier_resume_model)
    @optional_auth
    def get(self):
        """Récupère le résumé du panier"""
        try:
            user = get_current_user()
            if user:
                resume = panier_service.get_resume_panier_utilisateur(user['id'])
            else:
                session_id = request.headers.get('X-Session-ID', 'default')
                resume = panier_service.get_resume_panier_session(session_id)
            
            return resume
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du résumé: {e}")
            return {'message': 'Erreur lors de la récupération du résumé'}, 500


@panier_ns.route('/ajouter')
class AjouterAuPanierResource(Resource):
    @panier_ns.doc('ajouter_au_panier')
    @panier_ns.expect(ajouter_au_panier_model)
    @optional_auth
    @log_request_response
    def post(self):
        """Ajoute un produit au panier"""
        try:
            data = request.get_json()
            produit_id = data.get('produit_id')
            quantite = data.get('quantite', 1)
            
            logger.info(f"🛒 Ajout au panier | Produit ID: {produit_id} | Quantité: {quantite}")
            
            if not produit_id:
                logger.warning(f"❌ ID du produit manquant dans la requête: {data}")
                return {'message': 'ID du produit requis'}, 400
            
            user = get_current_user()
            session_id = request.headers.get('X-Session-ID', 'default')
            
            if user:
                # Utilisateur connecté
                logger.info(f"👤 Ajout pour utilisateur connecté: {user['id']}")
                log_business_operation('PanierService', 'ajouter_produit_utilisateur', 
                                     user_id=user['id'], data={'produit_id': produit_id, 'quantite': quantite})
                result = panier_service.ajouter_produit_utilisateur(user['id'], produit_id, quantite)
                
                if result['success']:
                    log_user_action('add_to_cart', user['id'], 
                                  produit_id=produit_id, quantite=quantite, 
                                  cart_id=result.get('panier', {}).get('id'))
                    logger.info(f"✅ Produit ajouté au panier utilisateur {user['id']}")
                else:
                    logger.warning(f"⚠️ Échec ajout panier utilisateur {user['id']}: {result.get('message')}")
            else:
                # Utilisateur non connecté
                logger.info(f"👻 Ajout pour utilisateur anonyme | Session: {session_id}")
                log_business_operation('PanierService', 'ajouter_produit_session', 
                                     data={'session_id': session_id, 'produit_id': produit_id, 'quantite': quantite})
                result = panier_service.ajouter_produit_session(session_id, produit_id, quantite)
                
                if result['success']:
                    log_user_action('add_to_cart_anonymous', None, 
                                  session_id=session_id, produit_id=produit_id, quantite=quantite,
                                  cart_id=result.get('panier', {}).get('id'))
                    logger.info(f"✅ Produit ajouté au panier session {session_id}")
                else:
                    logger.warning(f"⚠️ Échec ajout panier session {session_id}: {result.get('message')}")
            
            if result['success']:
                return result, 200
            else:
                return result, 400
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'ajout au panier: {e}")
            log_business_operation('PanierService', 'ajouter_produit', error=str(e))
            return {'message': 'Erreur lors de l\'ajout au panier'}, 500


@panier_ns.route('/modifier-quantite')
class ModifierQuantiteResource(Resource):
    @panier_ns.doc('modifier_quantite')
    @panier_ns.expect(modifier_quantite_model)
    @optional_auth
    def put(self):
        """Modifie la quantité d'un produit dans le panier"""
        try:
            data = request.get_json()
            produit_id = data.get('produit_id')
            quantite = data.get('quantite')
            
            if not produit_id or quantite is None:
                return {'message': 'ID du produit et quantité requis'}, 400
            
            user = get_current_user()
            if user:
                # Utilisateur connecté
                result = panier_service.modifier_quantite_utilisateur(user['id'], produit_id, quantite)
            else:
                # Utilisateur non connecté
                session_id = request.headers.get('X-Session-ID', 'default')
                result = panier_service.modifier_quantite_session(session_id, produit_id, quantite)
            
            if result['success']:
                return result, 200
            else:
                return result, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la modification de quantité: {e}")
            return {'message': 'Erreur lors de la modification de quantité'}, 500


@panier_ns.route('/supprimer')
class SupprimerDuPanierResource(Resource):
    @panier_ns.doc('supprimer_du_panier')
    @panier_ns.expect(supprimer_du_panier_model)
    @optional_auth
    def delete(self):
        """Supprime un produit du panier"""
        try:
            data = request.get_json()
            produit_id = data.get('produit_id')
            
            if not produit_id:
                return {'message': 'ID du produit requis'}, 400
            
            user = get_current_user()
            if user:
                # Utilisateur connecté
                result = panier_service.supprimer_produit_utilisateur(user['id'], produit_id)
            else:
                # Utilisateur non connecté
                session_id = request.headers.get('X-Session-ID', 'default')
                result = panier_service.supprimer_produit_session(session_id, produit_id)
            
            if result['success']:
                return result, 200
            else:
                return result, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la suppression: {e}")
            return {'message': 'Erreur lors de la suppression'}, 500


@panier_ns.route('/vider')
class ViderPanierResource(Resource):
    @panier_ns.doc('vider_panier')
    @optional_auth
    def delete(self):
        """Vide le panier"""
        try:
            user = get_current_user()
            if user:
                # Utilisateur connecté
                result = panier_service.vider_panier_utilisateur(user['id'])
            else:
                # Utilisateur non connecté
                session_id = request.headers.get('X-Session-ID', 'default')
                result = panier_service.vider_panier_session(session_id)
            
            if result['success']:
                return result, 200
            else:
                return result, 400
                
        except Exception as e:
            logger.error(f"Erreur lors du vidage: {e}")
            return {'message': 'Erreur lors du vidage'}, 500


@panier_ns.route('/migrer')
class MigrerPanierResource(Resource):
    @panier_ns.doc('migrer_panier')
    @token_required
    def post(self):
        """Migre un panier de session vers l'utilisateur connecté"""
        try:
            user = get_current_user()
            session_id = request.headers.get('X-Session-ID', 'default')
            result = panier_service.migrer_panier_session_vers_utilisateur(session_id, user['id'])
            
            if result['success']:
                return result, 200
            else:
                return result, 400
                
        except Exception as e:
            logger.error(f"Erreur lors de la migration: {e}")
            return {'message': 'Erreur lors de la migration'}, 500
