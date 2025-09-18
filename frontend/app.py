"""
Application Streamlit principale - Version Professionnelle
Architecture MVP (Model-View-Presenter)
Interface professionnelle avec authentification intégrée dans la sidebar
"""

import streamlit as st
import sys
import os

# Ajouter le répertoire courant au path pour les imports
sys.path.insert(0, os.path.dirname(__file__))

from views import (
    show_home, show_users, show_products,
    show_professional_sidebar, show_page_header
)
from views.cart_view import show_cart_page, show_cart_summary
from views.order_view import show_order_page, show_checkout_page, show_admin_orders
from views.auth_pro_view import show_auth, show_user_profile
from services.api_client import get_api_client
from services.auth_service import get_auth_service
from utils.logging_config import get_logger, log_navigation, log_user_action

# Configuration du logger
logger = get_logger(__name__)


def main():
    """Fonction principale de l'application"""
    
    # Configuration de la page
    st.set_page_config(
        page_title="E-commerce Pro",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialiser l'ID de session pour les utilisateurs anonymes
    if 'session_id' not in st.session_state:
        import uuid
        st.session_state['session_id'] = str(uuid.uuid4())
        logger.info(f"🆔 Session ID initialisé: {st.session_state['session_id']}")
    
    # Log du démarrage de l'application
    logger.info("🚀 Application Streamlit démarrée")
    
    # Style CSS global pour l'application
    st.markdown("""
    <style>
    /* Masquer le menu Streamlit par défaut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Style global */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Style pour les métriques */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #00d4aa;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4aa;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Style pour les cartes de contenu */
    .content-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Style pour les boutons */
    .stButton > button {
        background: linear-gradient(45deg, #00d4aa, #00a085);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #00a085, #00d4aa);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3);
    }
    
    /* Style pour les inputs */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00d4aa;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1);
    }
    
    /* Style pour les selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
    
    /* Style pour les tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Style pour les alertes */
    .stAlert {
        border-radius: 8px;
        border: none;
    }
    
    /* Style pour les colonnes */
    .stColumn {
        padding: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialiser la session state
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "🏠 Accueil"
    
    # Afficher la sidebar professionnelle
    show_professional_sidebar()
    
    # Contenu principal
    selected_page = st.session_state.get('selected_page', "🏠 Accueil")
    previous_page = st.session_state.get('previous_page', None)
    
    # Log de navigation si changement de page
    if previous_page != selected_page:
        log_navigation(previous_page or "None", selected_page)
        st.session_state['previous_page'] = selected_page
    
    # Router vers la page sélectionnée
    if selected_page == "🏠 Accueil":
        show_page_header("🏠 Accueil", "Tableau de bord principal de votre plateforme e-commerce")
        show_home()
        
    elif selected_page == "🔐 Connexion/Inscription":
        show_page_header("🔐 Authentification", "Connectez-vous ou créez un compte")
        show_auth()
        
    elif selected_page == "👤 Mon Profil":
        show_page_header("👤 Mon Profil", "Gérez vos informations personnelles")
        show_user_profile()
        
    elif selected_page == "📦 Produits":
        show_page_header("📦 Catalogue Produits", "Découvrez notre sélection de produits")
        show_products()
        
    elif selected_page == "🛒 Mon Panier":
        show_cart_page()
        
    elif selected_page == "🛒 Finaliser la commande":
        show_checkout_page()
        
    elif selected_page == "📦 Mes Commandes":
        show_page_header("📦 Mes Commandes", "Suivez vos commandes")
        show_order_page()
        
    elif selected_page == "📋 Commandes":
        # Vérifier les droits admin
        auth_service = get_auth_service()
        if auth_service.is_authenticated() and auth_service.is_admin():
            show_page_header("📋 Gestion des Commandes", "Administration des commandes clients")
            show_admin_orders()
        else:
            st.error("🔒 Accès refusé. Cette section est réservée aux administrateurs.")
            st.info("Connectez-vous avec un compte administrateur pour accéder à cette fonctionnalité.")
        
    elif selected_page == "👥 Utilisateurs":
        # Vérifier les droits admin
        auth_service = get_auth_service()
        if auth_service.is_authenticated() and auth_service.is_admin():
            show_page_header("👥 Gestion des Utilisateurs", "Administration des comptes utilisateurs")
            show_users()
        else:
            st.error("🔒 Accès refusé. Cette section est réservée aux administrateurs.")
            st.info("Connectez-vous avec un compte administrateur pour accéder à cette fonctionnalité.")
            
            
    
    else:
        st.error(f"Page non trouvée: {selected_page}")
        st.session_state.selected_page = "🏠 Accueil"
        st.rerun()


if __name__ == "__main__":
    main()
