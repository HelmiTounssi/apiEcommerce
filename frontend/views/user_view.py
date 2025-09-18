"""
Vue pour la gestion des utilisateurs
"""

import streamlit as st
from services.api_client import get_api_client
from services import UserService
from presenters import UserPresenter


def show_users():
    """Affiche la page de gestion des utilisateurs"""
    
    # Header style Back Market
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; font-size: 2.2rem; margin: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">👥 Gestion des Utilisateurs</h1>
        <p style="color: white; font-size: 1rem; margin: 0; opacity: 0.9; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">Clients et administrateurs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialiser les services
    api_client = get_api_client()
    user_service = UserService(api_client)
    user_presenter = UserPresenter(user_service)
    
    # Menu des actions avec design moderne
    st.markdown('<h2 class="section-title">🎯 Actions</h2>', unsafe_allow_html=True)
    
    action = st.selectbox(
        "Choisir une action",
        ["📋 Liste des utilisateurs", "➕ Créer un utilisateur", "🔍 Rechercher un utilisateur"],
        key="user_action",
        label_visibility="collapsed"
    )
    
    if action == "📋 Liste des utilisateurs":
        user_presenter.show_list()
    
    elif action == "➕ Créer un utilisateur":
        user_presenter.show_create_form()
    
    elif action == "🔍 Rechercher un utilisateur":
        show_user_search(user_presenter)
    
    # Gestion des actions contextuelles
    handle_user_actions(user_presenter)


def show_user_search(user_presenter: UserPresenter):
    """Affiche la recherche d'utilisateur"""
    st.subheader("🔍 Rechercher un Utilisateur")
    
    search_type = st.radio(
        "Type de recherche",
        ["Par ID", "Par email"],
        key="user_search_type"
    )
    
    if search_type == "Par ID":
        user_id = st.number_input("ID de l'utilisateur", min_value=1, key="user_id_search")
        if st.button("Rechercher", key="search_by_id"):
            if user_id:
                user_presenter.show_detail(user_id)
            else:
                st.error("Veuillez entrer un ID valide")
    
    else:  # Par email
        email = st.text_input("Email de l'utilisateur", key="user_email_search")
        if st.button("Rechercher", key="search_by_email"):
            if email:
                user = user_presenter.service.get_by_email(email)
                if user:
                    user_presenter.show_detail(user.id)
                else:
                    st.error("Utilisateur non trouvé")
            else:
                st.error("Veuillez entrer un email valide")


def handle_user_actions(user_presenter: UserPresenter):
    """Gère les actions contextuelles sur les utilisateurs"""
    
    # Vérifier les actions d'édition
    for key, value in st.session_state.items():
        if key.startswith("edit_user_") and value:
            user_id = int(key.split("_")[2])
            user_presenter.show_update_form(user_id)
            break
    
    # Vérifier les actions de gestion du stock
    for key, value in st.session_state.items():
        if key.startswith("manage_stock_") and value:
            product_id = int(key.split("_")[2])
            # Cette fonctionnalité sera implémentée dans le présentateur produit
            break
    
    # Vérifier l'affichage des commandes utilisateur
    if st.session_state.get("show_user_orders"):
        user_id = st.session_state["show_user_orders"]
        show_user_orders(user_id)


def show_user_orders(user_id: int):
    """Affiche les commandes d'un utilisateur"""
    st.subheader(f"🛒 Commandes de l'Utilisateur {user_id}")
    
    api_client = get_api_client()
    
    try:
        orders = api_client.get_orders_by_user(user_id)
        
        if not orders:
            st.info("Aucune commande trouvée pour cet utilisateur")
            return
        
        # Afficher les commandes
        for order in orders:
            with st.expander(f"Commande #{order['id']} - {order['statut']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Date:** {order['date_commande']}")
                    st.write(f"**Adresse:** {order['adresse_livraison']}")
                
                with col2:
                    st.write(f"**Statut:** {order['statut']}")
                    st.write(f"**Total:** {order.get('total', 'N/A')}€")
                
                # Lignes de commande
                if order.get('lignes_commande'):
                    st.write("**Articles:**")
                    for ligne in order['lignes_commande']:
                        st.write(f"- {ligne['quantite']}x Produit {ligne['produit_id']} - {ligne['prix_unitaire']}€")
    
    except Exception as e:
        st.error(f"Erreur lors du chargement des commandes: {str(e)}")
    
    # Bouton pour fermer
    if st.button("Fermer", key="close_user_orders"):
        st.session_state["show_user_orders"] = None
        st.rerun()
