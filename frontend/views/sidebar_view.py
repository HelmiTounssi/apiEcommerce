"""
Vue pour la sidebar professionnelle avec authentification
"""

import streamlit as st
from services.auth_service import get_auth_service


def show_professional_sidebar():
    """Affiche une sidebar professionnelle avec authentification intégrée"""
    
    # Style CSS pour la sidebar professionnelle
    st.markdown("""
    <style>
    .sidebar-auth-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .auth-user-info {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #00d4aa;
    }
    
    .auth-buttons {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .auth-button {
        background: linear-gradient(45deg, #00d4aa, #00a085);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        text-decoration: none;
        display: block;
    }
    
    .auth-button:hover {
        background: linear-gradient(45deg, #00a085, #00d4aa);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3);
    }
    
    .auth-button.secondary {
        background: linear-gradient(45deg, #6c757d, #495057);
    }
    
    .auth-button.secondary:hover {
        background: linear-gradient(45deg, #495057, #6c757d);
    }
    
    .user-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(45deg, #00d4aa, #00a085);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0 auto 1rem;
    }
    
    .user-role-badge {
        background: #00d4aa;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .user-role-badge.admin {
        background: #ff6b6b;
    }
    
    .nav-menu {
        margin-top: 2rem;
    }
    
    .nav-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #333;
        text-decoration: none;
        display: block;
    }
    
    .nav-item:hover {
        background: #f8f9fa;
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background: linear-gradient(45deg, #00d4aa, #00a085);
        color: white;
    }
    
    .nav-section-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 1.5rem 0 0.5rem 0;
        padding: 0 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Obtenir le service d'authentification
    auth_service = get_auth_service()
    is_authenticated = auth_service.is_authenticated()
    
    # Section d'authentification
    with st.sidebar:
        st.markdown('<div class="sidebar-auth-container">', unsafe_allow_html=True)
        
        if is_authenticated:
            # Utilisateur connecté
            user = auth_service.get_current_user()
            user_name = user.get('nom', 'Utilisateur') if user else 'Utilisateur'
            user_email = user.get('email', '') if user else ''
            user_role = user.get('role', 'client') if user else 'client'
            
            # S'assurer que user_role n'est jamais None
            if not user_role:
                user_role = 'client'
            
            # Avatar utilisateur
            st.markdown(f"""
            <div class="user-avatar">
                {user_name[0].upper() if user_name else 'U'}
            </div>
            """, unsafe_allow_html=True)
            
            # Informations utilisateur
            st.markdown(f"""
            <div class="auth-user-info">
                <h4 style="margin: 0 0 0.5rem 0; color: #333; font-size: 1.1rem;">{user_name}</h4>
                <p style="margin: 0 0 0.5rem 0; color: #666; font-size: 0.9rem;">{user_email}</p>
                <span class="user-role-badge {'admin' if user_role == 'admin' else ''}">{user_role.title() if user_role else 'Client'}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Boutons d'action
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("👤 Profil", key="profile_btn", use_container_width=True):
                    st.session_state.selected_page = "👤 Mon Profil"
                    st.rerun()
            
            with col2:
                if st.button("🚪 Déconnexion", key="logout_btn", use_container_width=True):
                    auth_service.logout()
                    st.success("Déconnexion réussie!")
                    st.rerun()
        
        else:
            # Utilisateur non connecté
            st.markdown("""
            <div style="text-align: center; color: white; margin-bottom: 1.5rem;">
                <h3 style="margin: 0; font-size: 1.2rem;">Bienvenue</h3>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Connectez-vous pour accéder à votre compte</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Boutons de connexion/inscription
            if st.button("🔐 Se connecter", key="login_btn", use_container_width=True):
                st.session_state.selected_page = "🔐 Connexion/Inscription"
                st.rerun()
            
            if st.button("📝 S'inscrire", key="register_btn", use_container_width=True):
                st.session_state.selected_page = "🔐 Connexion/Inscription"
                st.session_state.auth_tab = "Inscription"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Menu de navigation
        show_navigation_menu(is_authenticated, auth_service)


def show_navigation_menu(is_authenticated, auth_service):
    """Affiche le menu de navigation selon l'état d'authentification"""
    
    st.markdown('<div class="nav-menu">', unsafe_allow_html=True)
    
    # Menu de base (toujours visible)
    st.markdown('<div class="nav-section-title">Navigation</div>', unsafe_allow_html=True)
    
    if st.button("🏠 Accueil", key="home_btn", use_container_width=True):
        st.session_state.selected_page = "🏠 Accueil"
        st.rerun()
    
    # Panier pour utilisateurs non connectés
    if not is_authenticated:
        if st.button("🛒 Mon Panier", key="cart_btn", use_container_width=True):
            st.session_state.selected_page = "🛒 Mon Panier"
            st.rerun()
    
    # Menu pour utilisateurs connectés
    if is_authenticated:
        user = auth_service.get_current_user()
        user_role = user.get('role', 'client') if user else 'client'
        
        # S'assurer que user_role n'est jamais None
        if not user_role:
            user_role = 'client'
        
        # Panier (pas pour l'admin)
        if user_role != 'admin':
            if st.button("🛒 Mon Panier", key="cart_btn", use_container_width=True):
                st.session_state.selected_page = "🛒 Mon Panier"
                st.rerun()
        
        # Produits pour les clients (pas pour l'admin qui l'a dans Administration)
        if user_role != 'admin':
            if st.button("📦 Produits", key="products_btn", use_container_width=True):
                st.session_state.selected_page = "📦 Produits"
                st.rerun()
        
        st.markdown('<div class="nav-section-title">Mon Compte</div>', unsafe_allow_html=True)
        
        # Bouton commandes selon le rôle
        if user_role == 'admin':
            if st.button("📋 Commandes", key="orders_btn", use_container_width=True):
                st.session_state.selected_page = "📋 Commandes"
                st.rerun()
        else:
            if st.button("📦 Mes Commandes", key="orders_btn", use_container_width=True):
                st.session_state.selected_page = "📦 Mes Commandes"
                st.rerun()
        
        # Profil pour l'admin
        if user_role == 'admin':
            if st.button("👤 Profil", key="admin_profile_btn", use_container_width=True):
                st.session_state.selected_page = "👤 Profil"
                st.rerun()
        
        # Menu admin
        if user_role == 'admin':
            st.markdown('<div class="nav-section-title">Administration</div>', unsafe_allow_html=True)
            
            if st.button("📦 Produits", key="products_btn", use_container_width=True):
                st.session_state.selected_page = "📦 Produits"
                st.rerun()
            
            if st.button("👥 Utilisateurs", key="users_btn", use_container_width=True):
                st.session_state.selected_page = "👥 Utilisateurs"
                st.rerun()
            
            
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_page_header(page_title, page_description=""):
    """Affiche un en-tête de page professionnel"""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    ">
        <h1 style="margin: 0 0 0.5rem 0; font-size: 2.5rem; font-weight: 700;">{page_title}</h1>
        {f'<p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">{page_description}</p>' if page_description else ''}
    </div>
    """, unsafe_allow_html=True)

