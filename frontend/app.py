"""
Application principale Streamlit avec architecture MVP
"""

import streamlit as st
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from frontend.views import show_home, show_users, show_products, show_orders, show_auth, show_user_profile
from frontend.services.api_client import get_api_client
from frontend.services.auth_service import get_auth_service


def main():
    """Fonction principale de l'application"""
    
    # Configuration de la page
    st.set_page_config(
        page_title="E-commerce MVP",
        page_icon="🏪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS inspiré de Back Market
    st.markdown("""
    <style>
    /* Reset et base - Style Back Market */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
        max-width: 1400px;
    }
    
    /* Header Back Market style */
    .main-header {
        background: #00d4aa;
        padding: 1.5rem 2rem;
        border-radius: 0;
        margin: -1rem -1rem 0 -1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Navigation Back Market style */
    .nav-container {
        background: white;
        padding: 0;
        border-radius: 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 0;
    }
    
    /* Cartes produits Back Market style */
    .product-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.2s ease;
        border: 1px solid #f0f0f0;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        border-color: #00d4aa;
    }
    
    .product-image {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        background: #f8f9fa;
    }
    
    .product-title {
        font-size: 0.95rem;
        font-weight: 500;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
        line-height: 1.3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .product-price {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.25rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .product-price-old {
        font-size: 0.85rem;
        color: #8e8e93;
        text-decoration: line-through;
        margin-right: 0.5rem;
        font-weight: 400;
    }
    
    .product-status {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-bottom: 0.75rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .status-in-stock {
        background: #e8f5e8;
        color: #00d4aa;
        border: 1px solid #00d4aa;
    }
    
    .status-out-of-stock {
        background: #ffeaea;
        color: #ff6b6b;
        border: 1px solid #ff6b6b;
    }
    
    .product-rating {
        display: flex;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .stars {
        color: #ffc107;
        margin-right: 0.4rem;
        font-size: 0.8rem;
    }
    
    .rating-text {
        color: #8e8e93;
        font-size: 0.8rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Boutons Back Market style */
    .btn-primary {
        background: #00d4aa;
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 6px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 0.9rem;
    }
    
    .btn-primary:hover {
        background: #00b894;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0, 212, 170, 0.3);
    }
    
    .btn-secondary {
        background: white;
        color: #00d4aa;
        border: 1px solid #00d4aa;
        padding: 0.6rem 1.2rem;
        border-radius: 6px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        display: inline-block;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 0.9rem;
    }
    
    .btn-secondary:hover {
        background: #00d4aa;
        color: white;
        transform: translateY(-1px);
    }
    
    /* Métriques Back Market style */
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 3px solid #00d4aa;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.25rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .metric-label {
        color: #8e8e93;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Messages Back Market style */
    .success-message {
        background: #e8f5e8;
        color: #00d4aa;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        border: 1px solid #00d4aa;
        margin-bottom: 1rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .error-message {
        background: #ffeaea;
        color: #ff6b6b;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        border: 1px solid #ff6b6b;
        margin-bottom: 1rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .info-message {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        border: 1px solid #1976d2;
        margin-bottom: 1rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sidebar Back Market style */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    /* Sections Back Market style */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1.25rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #00d4aa;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Grille produits Back Market style */
    .products-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.25rem;
        margin-bottom: 2rem;
    }
    
    /* Badge de réduction */
    .discount-badge {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        background: #ff6b6b;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .products-grid {
            grid-template-columns: 1fr;
        }
        
        .product-card {
            padding: 0.75rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header principal style Back Market
    st.markdown("""
    <div class="main-header">
        <h1>🏪 E-commerce - Architecture MVP</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar de navigation style Back Market
    with st.sidebar:
        # Logo et titre
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 1rem; background: white; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🏪</div>
            <h3 style="color: #1a1a1a; margin: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">E-commerce</h3>
            <p style="color: #8e8e93; font-size: 0.85rem; margin: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">Architecture MVP</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Menu de navigation style Back Market
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <h4 style="color: #1a1a1a; margin: 0 0 1rem 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">🧭 Navigation</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Vérifier l'état d'authentification
        auth_service = get_auth_service()
        is_authenticated = auth_service.is_authenticated()
        
        # Menu de navigation selon l'état d'authentification
        if is_authenticated:
            user = auth_service.get_current_user()
            user_role = user.get('role') if user else None
            if not user_role:
                user_role = 'client'
            
            # Afficher les informations utilisateur
            user_name = user.get('nom', 'Utilisateur')
            user_email = user.get('email', '')
            user_role_display = user_role.title()
            
            st.markdown(f"""
            <div style="background: #e8f5e8; padding: 0.75rem; border-radius: 6px; margin-bottom: 1rem; border-left: 3px solid #00d4aa;">
                <p style="margin: 0; color: #1a1a1a; font-size: 0.9rem; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">
                    <strong>👤 {user_name}</strong><br>
                    <span style="color: #8e8e93;">{user_email}</span><br>
                    <span style="color: #00d4aa; font-weight: 600;">{user_role_display}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Menu pour utilisateur connecté
            menu_options = [
                "🏠 Accueil",
                "👤 Mon Profil",
                "📦 Produits",
                "🛒 Commandes"
            ]
            
            # Ajouter les options admin
            if user_role == 'admin':
                menu_options.extend([
                    "👥 Utilisateurs",
                    "📊 Statistiques",
                    "⚙️ Configuration"
                ])
            
            selected = st.selectbox(
                "Choisir une section",
                menu_options,
                key="navigation",
                label_visibility="collapsed"
            )
        else:
            # Menu pour utilisateur non connecté
            selected = st.selectbox(
                "Choisir une section",
                [
                    "🏠 Accueil",
                    "🔐 Connexion/Inscription",
                    "📦 Produits"
                ],
                key="navigation",
                label_visibility="collapsed"
            )
        
        st.markdown("---")
        
        # Statut de l'API style Back Market
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <h4 style="color: #1a1a1a; margin: 0 0 1rem 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">📡 Statut API</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Vérifier la connexion", use_container_width=True):
            try:
                api_client = get_api_client()
                response = api_client._make_request("GET", "/")
                if response:
                    st.success("✅ API connectée")
                else:
                    st.error("❌ API non disponible")
            except:
                st.error("❌ API non disponible")
        
        st.markdown("---")
        
        # Informations sur l'architecture style Back Market
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <h4 style="color: #1a1a1a; margin: 0 0 1rem 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">🏗️ Architecture</h4>
            <div style="background: #f8f9fa; padding: 0.75rem; border-radius: 6px; border-left: 3px solid #00d4aa;">
                <p style="margin: 0; font-size: 0.85rem; color: #1a1a1a; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">
                    <strong>Architecture MVP</strong><br>
                    • Models: Données<br>
                    • Services: Logique métier<br>
                    • Presenters: Présentation<br>
                    • Views: Interface
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Liens utiles style Back Market
        st.markdown("""
        <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <h4 style="color: #1a1a1a; margin: 0 0 1rem 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">🔗 Liens utiles</h4>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <a href="http://localhost:5000/docs/" target="_blank" style="color: #00d4aa; text-decoration: none; padding: 0.5rem; border-radius: 6px; background: #f8f9fa; transition: all 0.2s; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 0.85rem;">
                    📚 Documentation API
                </a>
                <a href="http://localhost:5000/api/" target="_blank" style="color: #00d4aa; text-decoration: none; padding: 0.5rem; border-radius: 6px; background: #f8f9fa; transition: all 0.2s; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 0.85rem;">
                    🌐 API REST
                </a>
                <a href="http://localhost:5000/" target="_blank" style="color: #00d4aa; text-decoration: none; padding: 0.5rem; border-radius: 6px; background: #f8f9fa; transition: all 0.2s; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 0.85rem;">
                    📊 Base de données
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Routage principal
    if selected == "🏠 Accueil":
        show_home()
    
    elif selected == "🔐 Connexion/Inscription":
        show_auth()
    
    elif selected == "👤 Mon Profil":
        if is_authenticated:
            show_user_profile()
        else:
            st.error("Vous devez être connecté pour accéder à cette page")
            st.info("Utilisez le menu pour vous connecter")
    
    elif selected == "👥 Utilisateurs":
        if is_authenticated and auth_service.is_admin():
            show_users()
        else:
            st.error("Accès refusé. Rôle administrateur requis.")
    
    elif selected == "📦 Produits":
        show_products()
    
    elif selected == "🛒 Commandes":
        if is_authenticated:
            show_orders()
        else:
            st.error("Vous devez être connecté pour accéder à cette page")
            st.info("Utilisez le menu pour vous connecter")
    
    elif selected == "📊 Statistiques":
        if is_authenticated and auth_service.is_admin():
            st.title("📊 Tableau de Bord")
            st.info("🚧 Cette section sera implémentée prochainement")
            
            # Placeholder pour les statistiques
            st.markdown("""
            ### Analyses disponibles:
            - Ventes par période
            - Produits les plus vendus
            - Performance des utilisateurs
            - Métriques de stock
            """)
        else:
            st.error("Accès refusé. Rôle administrateur requis.")
    
    elif selected == "⚙️ Configuration":
        if is_authenticated and auth_service.is_admin():
            st.title("⚙️ Configuration")
            st.info("🚧 Cette section sera implémentée prochainement")
            
            # Placeholder pour la configuration
            st.markdown("""
            ### Paramètres disponibles:
            - Configuration de l'API
            - Paramètres d'affichage
            - Gestion des utilisateurs
            - Sauvegarde des données
            """)
        else:
            st.error("Accès refusé. Rôle administrateur requis.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🏪 E-commerce MVP - Architecture Model-View-Presenter</p>
        <p>Backend: Flask + SQLAlchemy | Frontend: Streamlit</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
