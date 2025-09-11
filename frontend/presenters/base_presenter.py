"""
Présentateur de base pour tous les présentateurs
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
import streamlit as st


class BasePresenter(ABC):
    """Présentateur de base avec méthodes communes"""
    
    def __init__(self, service):
        self.service = service
    
    def show_loading(self, message: str = "Chargement..."):
        """Affiche un indicateur de chargement"""
        return st.spinner(message)
    
    def show_error(self, message: str):
        """Affiche un message d'erreur"""
        st.error(f"❌ {message}")
    
    def show_success(self, message: str):
        """Affiche un message de succès"""
        st.success(f"✅ {message}")
    
    def show_info(self, message: str):
        """Affiche un message d'information"""
        st.info(f"ℹ️ {message}")
    
    def show_warning(self, message: str):
        """Affiche un message d'avertissement"""
        st.warning(f"⚠️ {message}")
    
    def confirm_action(self, message: str) -> bool:
        """Demande confirmation pour une action"""
        return st.button(message, type="primary")
    
    def show_dataframe(self, data: List[Any], title: str = "Données"):
        """Affiche les données dans un DataFrame"""
        if not data:
            st.info("Aucune donnée à afficher")
            return
        
        import pandas as pd
        
        # Convertir les objets en dictionnaires
        if hasattr(data[0], 'to_dict'):
            df_data = [item.to_dict() for item in data]
        else:
            df_data = data
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
    
    def show_metrics(self, metrics: dict, title: str = "Métriques"):
        """Affiche des métriques"""
        if not metrics:
            return
        
        st.subheader(title)
        cols = st.columns(len(metrics))
        
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i]:
                st.metric(key, value)
    
    @abstractmethod
    def show_list(self):
        """Affiche la liste des éléments"""
        pass
    
    @abstractmethod
    def show_detail(self, item_id: int):
        """Affiche le détail d'un élément"""
        pass
    
    @abstractmethod
    def show_create_form(self):
        """Affiche le formulaire de création"""
        pass
    
    @abstractmethod
    def show_update_form(self, item_id: int):
        """Affiche le formulaire de mise à jour"""
        pass

