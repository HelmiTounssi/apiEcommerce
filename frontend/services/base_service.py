"""
Service de base pour tous les services
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import streamlit as st


class BaseService(ABC):
    """Service de base avec méthodes communes"""
    
    def __init__(self, api_client):
        self.api_client = api_client
    
    def handle_error(self, error: Exception, operation: str = "opération"):
        """Gère les erreurs de manière uniforme"""
        st.error(f"❌ Erreur lors de {operation}: {str(error)}")
    
    def show_success(self, message: str):
        """Affiche un message de succès"""
        st.success(f"✅ {message}")
    
    def show_info(self, message: str):
        """Affiche un message d'information"""
        st.info(f"ℹ️ {message}")
    
    def show_warning(self, message: str):
        """Affiche un message d'avertissement"""
        st.warning(f"⚠️ {message}")
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        """Récupère tous les éléments"""
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[Any]:
        """Récupère un élément par ID"""
        pass
    
    @abstractmethod
    def create(self, data: Any) -> Optional[Any]:
        """Crée un nouvel élément"""
        pass
    
    @abstractmethod
    def update(self, item_id: int, data: Any) -> Optional[Any]:
        """Met à jour un élément"""
        pass
    
    @abstractmethod
    def delete(self, item_id: int) -> bool:
        """Supprime un élément"""
        pass

