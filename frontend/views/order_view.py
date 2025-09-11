"""
Vue pour la gestion des commandes
"""

import streamlit as st
from ..services.api_client import get_api_client
from ..services import OrderService
from ..services.auth_service import get_auth_service
from ..presenters import OrderPresenter
from ..models import CreateOrderRequest, UpdateOrderRequest
from datetime import datetime


def show_orders():
    """Affiche la page de gestion des commandes"""
    
    # Vérifier l'authentification
    auth_service = get_auth_service()
    if not auth_service.is_authenticated():
        st.error("🔒 Vous devez être connecté pour accéder à cette page.")
        st.info("Utilisez le bouton de connexion dans la sidebar.")
        return
    
    user = auth_service.get_current_user()
    is_admin = auth_service.is_admin()
    
    # Header style Back Market
    if is_admin:
        title = "🛒 Gestion des Commandes"
        subtitle = "Administration - Toutes les commandes"
    else:
        title = "🛒 Mes Commandes"
        subtitle = f"Commandes de {user.get('nom', 'Utilisateur')}"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; font-size: 2.2rem; margin: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">{title}</h1>
        <p style="color: white; font-size: 1rem; margin: 0; opacity: 0.9; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialiser les services
    api_client = get_api_client()
    order_service = OrderService(api_client)
    order_presenter = OrderPresenter(order_service)
    
    # Charger les commandes selon le rôle
    if is_admin:
        # Admin : charger toutes les commandes
        if not order_presenter.load_orders():
            st.error("❌ Impossible de charger les commandes")
            return
    else:
        # Client : charger seulement ses commandes
        user_id = user.get('id')
        if not user_id:
            st.error("❌ Impossible de récupérer l'ID utilisateur")
            return
        
        # Charger les commandes de l'utilisateur
        user_orders = api_client.get_orders_by_user(user_id)
        if user_orders is None:
            st.error("❌ Impossible de charger vos commandes")
            return
        
        # Convertir en objets Order pour le presenter
        from ..models.order import Order
        orders = []
        for order_data in user_orders:
            order = Order(
                id=order_data['id'],
                utilisateur_id=order_data['utilisateur_id'],
                date_commande=order_data['date_commande'],
                adresse_livraison=order_data['adresse_livraison'],
                statut=order_data['statut']
            )
            orders.append(order)
        
        # Définir les commandes dans le presenter
        order_presenter.orders = orders
    
    # Menu des actions avec design moderne
    st.markdown('<h2 class="section-title">🎯 Actions</h2>', unsafe_allow_html=True)
    
    # Options selon le rôle
    if is_admin:
        action_options = [
            "📋 Voir toutes les commandes",
            "🔍 Filtrer les commandes",
            "➕ Créer une commande",
            "✏️ Modifier une commande",
            "🗑️ Supprimer une commande",
            "📊 Statistiques des commandes"
        ]
    else:
        action_options = [
            "📋 Voir mes commandes",
            "➕ Créer une commande",
            "📊 Mes statistiques"
        ]
    
    action = st.selectbox(
        "Choisir une action",
        action_options,
        key="order_action",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if action == "📋 Voir toutes les commandes" or action == "📋 Voir mes commandes":
        show_all_orders(order_presenter)
    
    elif action == "🔍 Filtrer les commandes":
        if is_admin:
            show_filtered_orders(order_presenter)
        else:
            st.info("🔒 Cette fonctionnalité est réservée aux administrateurs.")
    
    elif action == "➕ Créer une commande":
        show_create_order_form(order_presenter)
    
    elif action == "✏️ Modifier une commande":
        if is_admin:
            show_edit_order_form(order_presenter)
        else:
            st.info("🔒 Cette fonctionnalité est réservée aux administrateurs.")
    
    elif action == "🗑️ Supprimer une commande":
        if is_admin:
            show_delete_order_form(order_presenter)
        else:
            st.info("🔒 Cette fonctionnalité est réservée aux administrateurs.")
    
    elif action == "📊 Statistiques des commandes" or action == "📊 Mes statistiques":
        show_order_statistics(order_presenter)


def show_all_orders(order_presenter: OrderPresenter):
    """Affiche toutes les commandes ou les commandes de l'utilisateur"""
    
    # Vérifier si c'est un admin ou un client
    auth_service = get_auth_service()
    is_admin = auth_service.is_admin()
    
    if is_admin:
        st.subheader("📋 Toutes les Commandes")
    else:
        st.subheader("📋 Mes Commandes")
    
    orders = order_presenter.get_orders()
    
    if not orders:
        st.info("ℹ️ Aucune commande trouvée")
        return
    
    # Affichage des commandes
    for order in orders:
        with st.expander(f"Commande #{order.id} - {order_presenter.get_status_color(order.statut)} {order_presenter.get_status_display_name(order.statut)}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Utilisateur ID:** {order.utilisateur_id}")
                st.write(f"**Date:** {order.date_commande}")
            
            with col2:
                st.write(f"**Statut:** {order_presenter.get_status_display_name(order.statut)}")
                st.write(f"**Adresse:** {order.adresse_livraison}")
            
            with col3:
                if hasattr(order, 'total') and order.total:
                    st.write(f"**Total:** {order.total:.2f} €")
                
                # Boutons d'action
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("📝 Modifier", key=f"edit_{order.id}"):
                        st.session_state[f"edit_order_{order.id}"] = True
                
                with col_btn2:
                    if st.button("🗑️ Supprimer", key=f"delete_{order.id}"):
                        if order_presenter.delete_order(order.id):
                            st.rerun()
            
            # Afficher les lignes de commande si disponibles
            if hasattr(order, 'lignes_commande') and order.lignes_commande:
                st.write("**Lignes de commande:**")
                for ligne in order.lignes_commande:
                    st.write(f"- Produit {ligne.produit_id}: {ligne.quantite} x {ligne.prix_unitaire:.2f} €")


def show_filtered_orders(order_presenter: OrderPresenter):
    """Affiche les commandes filtrées"""
    
    st.subheader("🔍 Filtrer les Commandes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtre par statut
        statuses = ["tous"] + order_presenter.get_available_statuses()
        selected_status = st.selectbox(
            "Filtrer par statut",
            statuses,
            format_func=lambda x: "Tous les statuts" if x == "tous" else order_presenter.get_status_display_name(x)
        )
        order_presenter.set_filter_status(selected_status)
    
    with col2:
        # Filtre par utilisateur
        user_id = st.number_input(
            "Filtrer par ID utilisateur (0 pour tous)",
            min_value=0,
            value=0,
            step=1
        )
        order_presenter.set_filter_user(user_id if user_id > 0 else None)
    
    # Bouton pour effacer les filtres
    if st.button("🗑️ Effacer les filtres"):
        order_presenter.clear_filters()
        st.rerun()
    
    st.markdown("---")
    
    # Afficher les commandes filtrées
    filtered_orders = order_presenter.get_filtered_orders()
    
    if not filtered_orders:
        st.info("ℹ️ Aucune commande ne correspond aux critères de filtrage")
        return
    
    st.write(f"**{len(filtered_orders)} commande(s) trouvée(s)**")
    
    for order in filtered_orders:
        with st.expander(f"Commande #{order.id} - {order_presenter.get_status_color(order.statut)} {order_presenter.get_status_display_name(order.statut)}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Utilisateur ID:** {order.utilisateur_id}")
                st.write(f"**Date:** {order.date_commande}")
                st.write(f"**Adresse:** {order.adresse_livraison}")
            
            with col2:
                st.write(f"**Statut:** {order_presenter.get_status_display_name(order.statut)}")
                if hasattr(order, 'total') and order.total:
                    st.write(f"**Total:** {order.total:.2f} €")
                
                # Bouton pour changer le statut
                new_status = st.selectbox(
                    "Changer le statut",
                    order_presenter.get_available_statuses(),
                    key=f"status_{order.id}"
                )
                if st.button("🔄 Mettre à jour", key=f"update_status_{order.id}"):
                    if order_presenter.update_order_status(order.id, new_status):
                        st.rerun()


def show_create_order_form(order_presenter: OrderPresenter):
    """Affiche le formulaire de création de commande"""
    
    st.subheader("➕ Créer une Nouvelle Commande")
    
    with st.form("create_order_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            utilisateur_id = st.number_input(
                "ID Utilisateur",
                min_value=1,
                value=1,
                step=1
            )
            
            adresse_livraison = st.text_area(
                "Adresse de livraison",
                placeholder="Entrez l'adresse de livraison complète"
            )
        
        with col2:
            statut = st.selectbox(
                "Statut initial",
                order_presenter.get_available_statuses(),
                format_func=order_presenter.get_status_display_name
            )
        
        submitted = st.form_submit_button("✅ Créer la commande")
        
        if submitted:
            if not adresse_livraison.strip():
                st.error("❌ L'adresse de livraison est obligatoire")
            else:
                order_request = CreateOrderRequest(
                    utilisateur_id=utilisateur_id,
                    adresse_livraison=adresse_livraison,
                    statut=statut
                )
                
                new_order = order_presenter.create_order(order_request)
                if new_order:
                    st.success(f"✅ Commande #{new_order.id} créée avec succès !")
                    st.rerun()


def show_edit_order_form(order_presenter: OrderPresenter):
    """Affiche le formulaire de modification de commande"""
    
    st.subheader("✏️ Modifier une Commande")
    
    orders = order_presenter.get_orders()
    if not orders:
        st.info("ℹ️ Aucune commande à modifier")
        return
    
    # Sélection de la commande
    order_options = {f"Commande #{order.id} - {order_presenter.get_status_display_name(order.statut)}": order.id for order in orders}
    selected_order_name = st.selectbox("Sélectionner une commande", list(order_options.keys()))
    selected_order_id = order_options[selected_order_name]
    
    # Récupérer la commande
    order = order_presenter.get_order_by_id(selected_order_id)
    if not order:
        st.error("❌ Commande non trouvée")
        return
    
    with st.form("edit_order_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**ID:** {order.id}")
            st.write(f"**Utilisateur ID:** {order.utilisateur_id}")
            st.write(f"**Date de création:** {order.date_commande}")
            
            new_utilisateur_id = st.number_input(
                "Nouvel ID Utilisateur",
                min_value=1,
                value=order.utilisateur_id,
                step=1
            )
        
        with col2:
            new_adresse_livraison = st.text_area(
                "Nouvelle adresse de livraison",
                value=order.adresse_livraison
            )
            
            new_statut = st.selectbox(
                "Nouveau statut",
                order_presenter.get_available_statuses(),
                index=order_presenter.get_available_statuses().index(order.statut) if order.statut in order_presenter.get_available_statuses() else 0,
                format_func=order_presenter.get_status_display_name
            )
        
        submitted = st.form_submit_button("✅ Mettre à jour la commande")
        
        if submitted:
            if not new_adresse_livraison.strip():
                st.error("❌ L'adresse de livraison est obligatoire")
            else:
                update_request = UpdateOrderRequest(
                    utilisateur_id=new_utilisateur_id,
                    adresse_livraison=new_adresse_livraison,
                    statut=new_statut
                )
                
                updated_order = order_presenter.update_order(selected_order_id, update_request)
                if updated_order:
                    st.success(f"✅ Commande #{selected_order_id} mise à jour avec succès !")
                    st.rerun()


def show_delete_order_form(order_presenter: OrderPresenter):
    """Affiche le formulaire de suppression de commande"""
    
    st.subheader("🗑️ Supprimer une Commande")
    
    orders = order_presenter.get_orders()
    if not orders:
        st.info("ℹ️ Aucune commande à supprimer")
        return
    
    # Sélection de la commande
    order_options = {f"Commande #{order.id} - {order_presenter.get_status_display_name(order.statut)}": order.id for order in orders}
    selected_order_name = st.selectbox("Sélectionner une commande à supprimer", list(order_options.keys()))
    selected_order_id = order_options[selected_order_name]
    
    # Récupérer la commande
    order = order_presenter.get_order_by_id(selected_order_id)
    if not order:
        st.error("❌ Commande non trouvée")
        return
    
    # Affichage des détails de la commande
    st.warning("⚠️ **Attention : Cette action est irréversible !**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**ID:** {order.id}")
        st.write(f"**Utilisateur ID:** {order.utilisateur_id}")
        st.write(f"**Date:** {order.date_commande}")
    
    with col2:
        st.write(f"**Statut:** {order_presenter.get_status_display_name(order.statut)}")
        st.write(f"**Adresse:** {order.adresse_livraison}")
        if hasattr(order, 'total') and order.total:
            st.write(f"**Total:** {order.total:.2f} €")
    
    # Confirmation de suppression
    confirm = st.checkbox("Je confirme vouloir supprimer cette commande")
    
    if st.button("🗑️ Supprimer définitivement", disabled=not confirm):
        if order_presenter.delete_order(selected_order_id):
            st.success(f"✅ Commande #{selected_order_id} supprimée avec succès !")
            st.rerun()


def show_order_statistics(order_presenter: OrderPresenter):
    """Affiche les statistiques des commandes"""
    
    st.subheader("📊 Statistiques des Commandes")
    
    summary = order_presenter.get_orders_summary()
    
    if summary["total_orders"] == 0:
        st.info("ℹ️ Aucune commande pour afficher les statistiques")
        return
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total des commandes",
            value=summary["total_orders"]
        )
    
    with col2:
        st.metric(
            label="Valeur totale",
            value=f"{summary['total_value']:.2f} €"
        )
    
    with col3:
        st.metric(
            label="Valeur moyenne",
            value=f"{summary['average_value']:.2f} €"
        )
    
    with col4:
        st.metric(
            label="Statuts différents",
            value=len(summary["by_status"])
        )
    
    st.markdown("---")
    
    # Répartition par statut
    st.subheader("📈 Répartition par Statut")
    
    if summary["by_status"]:
        col1, col2 = st.columns(2)
        
        with col1:
            for status, count in summary["by_status"].items():
                percentage = (count / summary["total_orders"]) * 100
                st.write(f"{order_presenter.get_status_color(status)} **{order_presenter.get_status_display_name(status)}:** {count} ({percentage:.1f}%)")
        
        with col2:
            # Graphique simple avec des barres
            import pandas as pd
            
            df = pd.DataFrame([
                {"Statut": order_presenter.get_status_display_name(status), "Nombre": count}
                for status, count in summary["by_status"].items()
            ])
            
            st.bar_chart(df.set_index("Statut"))
    
    # Détails des commandes récentes
    st.subheader("🕒 Commandes Récentes")
    
    recent_orders = sorted(order_presenter.get_orders(), key=lambda x: x.date_commande, reverse=True)[:5]
    
    for order in recent_orders:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**Commande #{order.id}** - Utilisateur {order.utilisateur_id}")
        
        with col2:
            st.write(order_presenter.get_status_color(order.statut) + " " + order_presenter.get_status_display_name(order.statut))
        
        with col3:
            if hasattr(order, 'total') and order.total:
                st.write(f"{order.total:.2f} €")
            else:
                st.write("-")
