"""
Service pour la gestion du panier côté frontend
"""

import streamlit as st
import time
from typing import Dict, Any, Optional
# Pas d'héritage de BaseService car le panier a une logique différente
from models.cart import Cart, CartItem, CartSummary, AddToCartRequest, UpdateCartQuantityRequest, RemoveFromCartRequest
from utils.logging_config import get_logger, log_user_action, log_error

# Configuration du logger
logger = get_logger(__name__)

def log_api_call(method: str, url: str, status_code: int, 
                response_time: float, request_data: Optional[dict] = None, 
                response_data: Optional[dict] = None, error: Optional[str] = None):
    """Log un appel API côté frontend"""
    import json
    from datetime import datetime
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'url': url,
        'status_code': status_code,
        'response_time_ms': round(response_time * 1000, 2),
        'session_id': st.session_state.get('session_id', 'No-Session'),
        'user_authenticated': st.session_state.get('authenticated', False),
        'user_id': st.session_state.get('user_id', None)
    }
    
    if request_data:
        log_data['request_data'] = request_data
    if response_data:
        log_data['response_data'] = response_data
    if error:
        log_data['error'] = error
    
    logger.info(f"📡 API_CALL | {json.dumps(log_data, ensure_ascii=False)}")


class CartService:
    """Service pour la gestion du panier"""
    
    def __init__(self):
        from services.api_client import get_api_client
        self.api_client = get_api_client()
        self.api_base_url = "http://localhost:5000"
        self.base_url = f"{self.api_base_url}/panier"
    
    def _get_headers(self, token: Optional[str] = None, include_content_type: bool = True) -> Dict[str, str]:
        """Crée les headers pour les requêtes API"""
        headers = {}
        if include_content_type:
            headers['Content-Type'] = 'application/json'
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return headers
    
    def get_cart(self, token: Optional[str] = None) -> Dict[str, Any]:
        """Récupère le panier de l'utilisateur ou de la session"""
        try:
            headers = self._get_headers(token, include_content_type=False)
            session_id = st.session_state.get('session_id', 'default')
            headers['X-Session-ID'] = session_id
            
            data = self.api_client.get_cart(headers)
            
            if data is not None:
                if 'message' in data and data['message'] == 'Panier vide':
                    return {'success': True, 'cart': None, 'message': 'Panier vide'}
                else:
                    return {'success': True, 'cart': Cart.from_dict(data)}
            else:
                return {'success': False, 'message': 'Erreur lors de la récupération du panier'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la récupération du panier: {str(e)}'}
    
    def get_cart_summary(self, token: Optional[str] = None) -> Dict[str, Any]:
        """Récupère le résumé du panier"""
        try:
            headers = self._get_headers(token, include_content_type=False)
            session_id = st.session_state.get('session_id', 'default')
            headers['X-Session-ID'] = session_id
            
            data = self.api_client.get_cart_summary(headers)
            
            if data is not None:
                return {'success': True, 'summary': CartSummary.from_dict(data)}
            else:
                return {'success': False, 'message': 'Erreur lors de la récupération du résumé'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la récupération du résumé: {str(e)}'}
    
    def add_to_cart(self, produit_id: int, quantite: int = 1, token: Optional[str] = None) -> Dict[str, Any]:
        """Ajoute un produit au panier"""
        start_time = time.time()
        
        try:
            logger.info(f"🛒 Début ajout au panier | Produit ID: {produit_id} | Quantité: {quantite}")
            
            headers = self._get_headers(token)
            session_id = st.session_state.get('session_id', 'default')
            headers['X-Session-ID'] = session_id
            
            request_data = AddToCartRequest(produit_id=produit_id, quantite=quantite)
            
            # Log de l'appel API
            logger.info(f"📡 Appel API add_to_cart | URL: {self.base_url}/ajouter | Session: {session_id}")
            
            data = self.api_client.add_to_cart(request_data.to_dict(), headers)
            response_time = time.time() - start_time
            
            # Log de la réponse API
            log_api_call(
                method='POST',
                url=f"{self.base_url}/ajouter",
                status_code=200 if data else 500,
                response_time=response_time,
                request_data=request_data.to_dict(),
                response_data=data
            )
            
            if data is not None:
                if data.get('success', False):
                    logger.info(f"✅ Produit ajouté avec succès | Produit ID: {produit_id}")
                    log_user_action('add_to_cart_success', 
                                  produit_id=produit_id, quantite=quantite, 
                                  response_time=response_time)
                    return {'success': True, 'message': data.get('message', 'Produit ajouté au panier')}
                else:
                    error_msg = data.get('message', 'Erreur lors de l\'ajout')
                    logger.warning(f"⚠️ Échec ajout au panier | Produit ID: {produit_id} | Erreur: {error_msg}")
                    log_user_action('add_to_cart_failed', 
                                  produit_id=produit_id, quantite=quantite, 
                                  error=error_msg, response_time=response_time)
                    return {'success': False, 'message': error_msg}
            else:
                error_msg = 'Erreur lors de l\'ajout au panier'
                logger.error(f"❌ Réponse API nulle | Produit ID: {produit_id}")
                log_api_call(
                    method='POST',
                    url=f"{self.base_url}/ajouter",
                    status_code=500,
                    response_time=response_time,
                    request_data=request_data.to_dict(),
                    error=error_msg
                )
                return {'success': False, 'message': error_msg}
                
        except Exception as e:
            response_time = time.time() - start_time
            error_msg = f'Erreur lors de l\'ajout au panier: {str(e)}'
            logger.error(f"❌ Exception lors de l'ajout au panier | Produit ID: {produit_id} | Erreur: {str(e)}")
            log_error(e, "add_to_cart", produit_id=produit_id, quantite=quantite, response_time=response_time)
            return {'success': False, 'message': error_msg}
    
    def update_quantity(self, produit_id: int, quantite: int, token: Optional[str] = None) -> Dict[str, Any]:
        """Modifie la quantité d'un produit dans le panier"""
        try:
            headers = self._get_headers(token)
            session_id = st.session_state.get('session_id', 'default')
            headers['X-Session-ID'] = session_id
            
            request_data = UpdateCartQuantityRequest(produit_id=produit_id, quantite=quantite)
            
            data = self.api_client.update_cart_quantity(request_data.to_dict(), headers)
            
            if data is not None:
                if data.get('success', False):
                    return {'success': True, 'message': data.get('message', 'Quantité modifiée')}
                else:
                    return {'success': False, 'message': data.get('message', 'Erreur lors de la modification')}
            else:
                return {'success': False, 'message': 'Erreur lors de la modification'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la modification: {str(e)}'}
    
    def remove_from_cart(self, produit_id: int, token: Optional[str] = None) -> Dict[str, Any]:
        """Supprime un produit du panier"""
        try:
            headers = self._get_headers(token)
            session_id = st.session_state.get('session_id', 'default')
            headers['X-Session-ID'] = session_id
            
            request_data = RemoveFromCartRequest(produit_id=produit_id)
            
            data = self.api_client.remove_from_cart(request_data.to_dict(), headers)
            
            if data is not None:
                if data.get('success', False):
                    return {'success': True, 'message': data.get('message', 'Produit supprimé du panier')}
                else:
                    return {'success': False, 'message': data.get('message', 'Erreur lors de la suppression')}
            else:
                return {'success': False, 'message': 'Erreur lors de la suppression'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la suppression: {str(e)}'}
    
    def clear_cart(self, token: Optional[str] = None) -> Dict[str, Any]:
        """Vide le panier"""
        try:
            headers = self._get_headers(token)
            session_id = st.session_state.get('session_id', 'default')
            headers['X-Session-ID'] = session_id
            
            data = self.api_client.clear_cart(headers)
            
            if data is not None:
                if data.get('success', False):
                    return {'success': True, 'message': data.get('message', 'Panier vidé')}
                else:
                    return {'success': False, 'message': data.get('message', 'Erreur lors du vidage')}
            else:
                return {'success': False, 'message': 'Erreur lors du vidage'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors du vidage: {str(e)}'}
    
    def migrate_cart(self, token: str) -> Dict[str, Any]:
        """Migre le panier de session vers l'utilisateur connecté"""
        try:
            headers = self._get_headers(token)
            session_id = st.session_state.get('session_id', 'default')
            headers['X-Session-ID'] = session_id
            
            data = self.api_client.migrate_cart(headers)
            
            if data is not None:
                if data.get('success', False):
                    return {'success': True, 'message': data.get('message', 'Panier migré avec succès')}
                else:
                    return {'success': False, 'message': data.get('message', 'Erreur lors de la migration')}
            else:
                return {'success': False, 'message': 'Erreur lors de la migration'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la migration: {str(e)}'}
    
    def get_cart_item_count(self, token: Optional[str] = None) -> int:
        """Récupère le nombre d'items dans le panier"""
        try:
            summary_result = self.get_cart_summary(token)
            if summary_result['success']:
                return summary_result['summary'].nombre_items
            return 0
        except Exception:
            return 0
    
    def get_cart_total(self, token: Optional[str] = None) -> float:
        """Récupère le total du panier"""
        try:
            summary_result = self.get_cart_summary(token)
            if summary_result['success']:
                return summary_result['summary'].total
            return 0.0
        except Exception:
            return 0.0


# Instance globale du service
cart_service = CartService()


def get_cart_service() -> CartService:
    """Retourne l'instance du service panier"""
    return cart_service
