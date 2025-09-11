"""
Client API pour les appels HTTP
"""

import requests
from typing import Dict, Any, Optional, List
import streamlit as st


class ApiClient:
    """Client API pour les appels HTTP vers le backend"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def is_authenticated(self) -> bool:
        """Vérifie si l'utilisateur est authentifié"""
        return 'access_token' in st.session_state and st.session_state.get('is_authenticated', False)
    
    def get_auth_info(self) -> Dict[str, Any]:
        """Récupère les informations d'authentification"""
        return {
            'is_authenticated': self.is_authenticated(),
            'has_token': 'access_token' in st.session_state,
            'user': st.session_state.get('user', None),
            'token_preview': st.session_state.get('access_token', '')[:20] + '...' if 'access_token' in st.session_state else 'None'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Effectue une requête HTTP avec authentification"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            # Récupérer le token JWT depuis la session Streamlit
            headers = {}
            if 'access_token' in st.session_state:
                headers['Authorization'] = f"Bearer {st.session_state['access_token']}"
                # Debug: afficher si le token est présent
                if method.upper() in ['POST', 'PUT', 'DELETE']:
                    st.info(f"🔐 Token JWT envoyé pour {method} {endpoint}")
            else:
                # Debug: afficher si le token est manquant
                if method.upper() in ['POST', 'PUT', 'DELETE']:
                    st.warning(f"⚠️ Aucun token JWT trouvé pour {method} {endpoint}")
            
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Méthode HTTP non supportée: {method}")
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erreur API: {str(e)}")
            return None
        except Exception as e:
            st.error(f"❌ Erreur inattendue: {str(e)}")
            return None
    
    # Méthodes pour les utilisateurs
    def get_users(self) -> List[Dict]:
        """Récupère tous les utilisateurs"""
        response = self._make_request("GET", "/api/utilisateurs/")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Récupère un utilisateur par ID"""
        response = self._make_request("GET", f"/api/utilisateurs/{user_id}")
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Crée un nouvel utilisateur"""
        response = self._make_request("POST", "/api/utilisateurs", user_data)
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def update_user(self, user_id: int, user_data: Dict) -> Optional[Dict]:
        """Met à jour un utilisateur"""
        response = self._make_request("PUT", f"/api/utilisateurs/{user_id}", user_data)
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def delete_user(self, user_id: int) -> bool:
        """Supprime un utilisateur"""
        response = self._make_request("DELETE", f"/api/utilisateurs/{user_id}")
        return response is not None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Récupère un utilisateur par email"""
        response = self._make_request("GET", f"/api/utilisateurs/email/{email}")
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def get_users_by_role(self, role: str) -> List[Dict]:
        """Récupère les utilisateurs par rôle"""
        response = self._make_request("GET", f"/api/utilisateurs/role/{role}")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    # Méthodes pour les produits
    def get_products(self) -> List[Dict]:
        """Récupère tous les produits"""
        response = self._make_request("GET", "/api/produits/")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """Récupère un produit par ID"""
        response = self._make_request("GET", f"/api/produits/{product_id}")
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def create_product(self, product_data: Dict) -> Optional[Dict]:
        """Crée un nouveau produit"""
        response = self._make_request("POST", "/api/produits", product_data)
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def update_product(self, product_id: int, product_data: Dict) -> Optional[Dict]:
        """Met à jour un produit"""
        response = self._make_request("PUT", f"/api/produits/{product_id}", product_data)
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def delete_product(self, product_id: int) -> bool:
        """Supprime un produit"""
        response = self._make_request("DELETE", f"/api/produits/{product_id}")
        return response is not None
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """Récupère les produits par catégorie"""
        response = self._make_request("GET", f"/api/produits/categorie/{category}")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    def get_products_in_stock(self) -> List[Dict]:
        """Récupère les produits en stock"""
        response = self._make_request("GET", "/api/produits/stock")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    def get_products_by_price_range(self, min_price: float, max_price: float) -> List[Dict]:
        """Récupère les produits dans une fourchette de prix"""
        response = self._make_request("GET", f"/api/produits/prix/{min_price}/{max_price}")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Met à jour le stock d'un produit"""
        data = {"quantite": quantity}
        response = self._make_request("PUT", f"/api/produits/{product_id}/stock", data)
        return response is not None
    
    # Méthodes pour les commandes
    def get_orders(self) -> List[Dict]:
        """Récupère toutes les commandes"""
        response = self._make_request("GET", "/api/commandes/")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    def get_order(self, order_id: int) -> Optional[Dict]:
        """Récupère une commande par ID"""
        response = self._make_request("GET", f"/api/commandes/{order_id}")
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def get_user_orders(self, user_id: int) -> List[Dict]:
        """Récupère les commandes d'un utilisateur"""
        response = self._make_request("GET", f"/api/commandes/utilisateur/{user_id}")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    def create_order(self, order_data: Dict) -> Optional[Dict]:
        """Crée une nouvelle commande"""
        response = self._make_request("POST", "/api/commandes", order_data)
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def update_order(self, order_id: int, order_data: Dict) -> Optional[Dict]:
        """Met à jour une commande"""
        response = self._make_request("PUT", f"/api/commandes/{order_id}", order_data)
        if response is None:
            return None
        # L'API retourne directement un dictionnaire, pas un objet avec clé 'data'
        if isinstance(response, dict):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data') if hasattr(response, 'get') else None
    
    def delete_order(self, order_id: int) -> bool:
        """Supprime une commande"""
        response = self._make_request("DELETE", f"/api/commandes/{order_id}")
        return response is not None
    
    def get_orders_by_user(self, user_id: int) -> List[Dict]:
        """Récupère les commandes d'un utilisateur"""
        response = self._make_request("GET", f"/api/commandes/utilisateur/{user_id}")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    def get_orders_by_status(self, status: str) -> List[Dict]:
        """Récupère les commandes par statut"""
        response = self._make_request("GET", f"/api/commandes/statut/{status}")
        if response is None:
            return []
        # L'API retourne directement une liste, pas un objet avec clé 'data'
        if isinstance(response, list):
            return response
        # Fallback si c'est un objet avec clé 'data'
        return response.get('data', []) if isinstance(response, dict) else []
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Met à jour le statut d'une commande"""
        data = {"statut": status}
        response = self._make_request("PUT", f"/api/commandes/{order_id}/statut", data)
        return response is not None
    
    def get_order_total(self, order_id: int) -> Optional[float]:
        """Récupère le total d'une commande"""
        response = self._make_request("GET", f"/api/commandes/{order_id}/total")
        if response is None:
            return None
        # L'API retourne un objet avec le total
        if isinstance(response, dict):
            return response.get('total')
        return None


def get_api_client() -> ApiClient:
    """Factory function pour créer un client API"""
    return ApiClient()
