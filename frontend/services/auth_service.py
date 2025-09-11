"""
Service d'authentification pour le frontend
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any
from .api_client import get_api_client


class AuthService:
    """Service pour la gestion de l'authentification côté frontend"""
    
    def __init__(self):
        self.api_client = get_api_client()
        self.base_url = "http://localhost:5000"
    
    def register(self, email: str, password: str, nom: str, role: str = "client") -> Dict[str, Any]:
        """
        Inscrit un nouvel utilisateur
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe
            nom: Nom de l'utilisateur
            role: Rôle (client ou admin)
            
        Returns:
            Dict contenant le résultat de l'inscription
        """
        try:
            data = {
                "email": email,
                "mot_de_passe": password,
                "nom": nom,
                "role": role
            }
            
            response = requests.post(f"{self.base_url}/api/auth/register", json=data)
            
            if response.status_code == 201:
                result = response.json()
                # Stocker le token dans la session
                st.session_state['access_token'] = result['access_token']
                st.session_state['user'] = result['user']
                st.session_state['is_authenticated'] = True
                
                return {
                    'success': True,
                    'message': 'Inscription réussie !',
                    'user': result['user']
                }
            else:
                error_data = response.json()
                return {
                    'success': False,
                    'message': error_data.get('message', 'Erreur lors de l\'inscription'),
                    'error': error_data.get('error', 'unknown_error')
                }
                
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'message': 'Impossible de se connecter au serveur',
                'error': 'connection_error'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur: {str(e)}',
                'error': 'internal_error'
            }
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Connecte un utilisateur
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe
            
        Returns:
            Dict contenant le résultat de la connexion
        """
        try:
            data = {
                "email": email,
                "mot_de_passe": password
            }
            
            response = requests.post(f"{self.base_url}/api/auth/login", json=data)
            
            if response.status_code == 200:
                result = response.json()
                # Stocker le token dans la session
                st.session_state['access_token'] = result['access_token']
                st.session_state['user'] = result['user']
                st.session_state['is_authenticated'] = True
                
                return {
                    'success': True,
                    'message': 'Connexion réussie !',
                    'user': result['user']
                }
            else:
                error_data = response.json()
                return {
                    'success': False,
                    'message': error_data.get('message', 'Erreur lors de la connexion'),
                    'error': error_data.get('error', 'unknown_error')
                }
                
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'message': 'Impossible de se connecter au serveur',
                'error': 'connection_error'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur: {str(e)}',
                'error': 'internal_error'
            }
    
    def logout(self):
        """Déconnecte l'utilisateur"""
        # Supprimer les données de session
        if 'access_token' in st.session_state:
            del st.session_state['access_token']
        if 'user' in st.session_state:
            del st.session_state['user']
        if 'is_authenticated' in st.session_state:
            del st.session_state['is_authenticated']
        
        st.success("Déconnexion réussie !")
        st.rerun()
    
    def is_authenticated(self) -> bool:
        """Vérifie si l'utilisateur est connecté"""
        return st.session_state.get('is_authenticated', False)
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Récupère l'utilisateur actuellement connecté"""
        return st.session_state.get('user', None)
    
    def get_access_token(self) -> Optional[str]:
        """Récupère le token d'accès"""
        return st.session_state.get('access_token', None)
    
    def verify_token(self) -> bool:
        """Vérifie la validité du token actuel"""
        token = self.get_access_token()
        if not token:
            return False
        
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{self.base_url}/api/auth/verify", headers=headers)
            
            if response.status_code == 200:
                return True
            else:
                # Token invalide, déconnecter l'utilisateur
                self.logout()
                return False
                
        except Exception:
            return False
    
    def is_admin(self) -> bool:
        """Vérifie si l'utilisateur actuel est un administrateur"""
        user = self.get_current_user()
        return user and user.get('role') == 'admin'
    
    def is_client(self) -> bool:
        """Vérifie si l'utilisateur actuel est un client"""
        user = self.get_current_user()
        return user and user.get('role') == 'client'


def get_auth_service() -> AuthService:
    """Factory function pour obtenir le service d'authentification"""
    return AuthService()

