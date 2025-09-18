"""
Vue pour la gestion des commandes
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from datetime import datetime
from services.order_service import OrderService
from services.cart_service import get_cart_service
from services.auth_service import get_auth_service
from models.order import Order, CreateOrderRequest, OrderLine
from models.cart import Cart, CartItem


def show_order_page():
    """Affiche la page des commandes"""
    st.title("📦 Mes Commandes")
    st.markdown("---")
    
    auth_service = get_auth_service()
    
    if not auth_service.is_authenticated():
        st.info("🔐 Connectez-vous pour voir vos commandes")
        if st.button("🔑 Se connecter", type="primary"):
            st.session_state['selected_page'] = "🔐 Connexion"
            st.rerun()
        return
    
    # Récupérer les commandes de l'utilisateur
    user_info = auth_service.get_current_user()
    if not user_info:
        st.error("❌ Impossible de récupérer les informations utilisateur")
        return
    
    user_id = user_info.get('id')
    if not user_id:
        st.error("❌ Impossible de récupérer l'ID utilisateur")
        return
    
    from services.api_client import get_api_client
    api_client = get_api_client()
    order_service = OrderService(api_client)
    orders = order_service.get_by_user(user_id)
    
    if not orders:
        st.info("📦 Vous n'avez pas encore passé de commande")
        st.markdown("Découvrez nos produits et ajoutez-les à votre panier !")
        
        if st.button("🛍️ Voir les produits", type="primary"):
            st.session_state['selected_page'] = "🛍️ Produits"
            st.rerun()
        return
    
    # Afficher les commandes
    st.subheader(f"📋 {len(orders)} commande(s)")
    
    for order in orders:
        show_order_card(order)


def show_order_card(order: Order):
    """Affiche une carte de commande"""
    with st.container():
        # Header de la commande
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**Commande #{order.id}**")
            if order.date_commande:
                st.markdown(f"📅 {order.date_commande.strftime('%d/%m/%Y %H:%M')}")
        
        with col2:
            # Statut avec couleur
            status_colors = {
                "en_attente": "🟡",
                "confirme": "🔵", 
                "expedie": "🟢",
                "annulee": "🔴"
            }
            status_emoji = status_colors.get(order.statut, "⚪")
            st.markdown(f"{status_emoji} **{order.statut.replace('_', ' ').title()}**")
        
        with col3:
            st.markdown(f"**€{order.total:.2f}**")
        
        # Détails de la commande
        with st.expander("Voir les détails"):
            st.markdown(f"**Adresse de livraison:** {order.adresse_livraison}")
            
            if order.lignes_commande:
                st.markdown("**Articles:**")
                for ligne in order.lignes_commande:
                    st.markdown(f"• {ligne.quantite}x Produit #{ligne.produit_id} - €{ligne.prix_unitaire:.2f} = €{ligne.total_ligne:.2f}")
        
        st.markdown("---")


def show_checkout_page():
    """Affiche la page de finalisation de commande"""
    st.title("🛒 Finaliser la commande")
    st.markdown("---")
    
    auth_service = get_auth_service()
    cart_service = get_cart_service()
    
    if not auth_service.is_authenticated():
        st.error("❌ Vous devez être connecté pour passer commande")
        if st.button("🔑 Se connecter", type="primary"):
            st.session_state['selected_page'] = "🔐 Connexion"
            st.rerun()
        return
    
    # Récupérer le panier
    token = auth_service.get_access_token()
    cart_result = cart_service.get_cart(token)
    
    if not cart_result['success']:
        st.error(f"❌ Erreur lors de la récupération du panier: {cart_result['message']}")
        return
    
    cart = cart_result.get('cart')
    
    if not cart or not cart.items:
        st.info("🛒 Votre panier est vide")
        if st.button("🛍️ Voir les produits", type="primary"):
            st.session_state['selected_page'] = "🛍️ Produits"
            st.rerun()
        return
    
    # Afficher le résumé de la commande
    st.subheader("📋 Résumé de votre commande")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Liste des articles
        st.markdown("**Articles:**")
        for item in cart.items:
            from utils.product_utils import get_product_name
            nom_produit = get_product_name(item.produit, f"Produit #{item.produit_id}")
            st.markdown(f"• {item.quantite}x {nom_produit} - €{item.prix_unitaire:.2f}")
    
    with col2:
        st.markdown(f"**Nombre d'articles:** {cart.nombre_items}")
        st.markdown(f"**Total:** €{cart.total:.2f}")
    
    st.markdown("---")
    
    # Formulaire de commande
    st.subheader("📝 Informations de livraison")
    
    # Récupérer les informations utilisateur
    user_info = auth_service.get_current_user()
    default_nom = user_info.get('nom', '') if user_info else ''
    default_prenom = user_info.get('prenom', '') if user_info else ''
    default_email = user_info.get('email', '') if user_info else ''
    default_telephone = user_info.get('telephone', '') if user_info else ''
    default_adresse = user_info.get('adresse', '') if user_info else ''
    
    # Formulaire
    with st.form("checkout_form"):
        st.markdown("**👤 Informations personnelles**")
        
        col1, col2 = st.columns(2)
        with col1:
            nom_livraison = st.text_input(
                "Nom de famille *",
                value=default_nom,
                placeholder="Votre nom de famille",
                help="Nom de famille pour la livraison"
            )
        
        with col2:
            prenom_livraison = st.text_input(
                "Prénom *",
                value=default_prenom,
                placeholder="Votre prénom",
                help="Prénom pour la livraison"
            )
        
        col3, col4 = st.columns(2)
        with col3:
            email_livraison = st.text_input(
                "Email de contact *",
                value=default_email,
                placeholder="votre.email@example.com",
                help="Email pour les notifications de livraison"
            )
        
        with col4:
            telephone_livraison = st.text_input(
                "Téléphone *",
                value=default_telephone,
                placeholder="06 12 34 56 78",
                help="Numéro de téléphone pour la livraison"
            )
        
        st.markdown("**🏠 Adresse de livraison**")
        
        adresse_livraison = st.text_area(
            "Adresse complète *",
            value=default_adresse,
            placeholder="Numéro et nom de rue\nCode postal, ville\nPays",
            height=100,
            help="Adresse complète de livraison"
        )
        
        col5, col6 = st.columns(2)
        with col5:
            code_postal = st.text_input(
                "Code postal *",
                placeholder="75001",
                help="Code postal de livraison"
            )
        
        with col6:
            ville = st.text_input(
                "Ville *",
                placeholder="Paris",
                help="Ville de livraison"
            )
        
        pays = st.selectbox(
            "Pays *",
            ["France", "Belgique", "Suisse", "Canada", "Autre"],
            help="Pays de livraison"
        )
        
        st.markdown("**📦 Options de livraison**")
        
        mode_livraison = st.selectbox(
            "Mode de livraison",
            ["Standard (3-5 jours) - Gratuit", "Express (1-2 jours) - +5€", "Point relais - Gratuit"],
            help="Choisissez votre mode de livraison"
        )
        
        instructions_livraison = st.text_area(
            "Instructions spéciales (optionnel)",
            placeholder="Ex: Sonner à l'interphone, laisser chez le voisin, etc.",
            height=60,
            help="Instructions particulières pour le livreur"
        )
        
        # Conditions générales
        accept_conditions = st.checkbox(
            "J'accepte les conditions générales de vente",
            help="Vous devez accepter les conditions pour continuer"
        )
        
        # Bouton de validation
        submitted = st.form_submit_button(
            "🛒 Confirmer la commande",
            type="primary",
            use_container_width=True
        )
    
    # Traitement de la soumission du formulaire
    if submitted:
        # Validation des champs obligatoires
        errors = []
        
        if not nom_livraison.strip():
            errors.append("❌ Le nom de famille est obligatoire")
        if not prenom_livraison.strip():
            errors.append("❌ Le prénom est obligatoire")
        if not email_livraison.strip():
            errors.append("❌ L'email est obligatoire")
        elif "@" not in email_livraison:
            errors.append("❌ L'email n'est pas valide")
        if not telephone_livraison.strip():
            errors.append("❌ Le téléphone est obligatoire")
        if not adresse_livraison.strip():
            errors.append("❌ L'adresse est obligatoire")
        if not code_postal.strip():
            errors.append("❌ Le code postal est obligatoire")
        if not ville.strip():
            errors.append("❌ La ville est obligatoire")
        if not accept_conditions:
            errors.append("❌ Vous devez accepter les conditions générales")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Créer l'objet d'adresse de livraison détaillé
            adresse_complete = {
                "nom": nom_livraison.strip(),
                "prenom": prenom_livraison.strip(),
                "email": email_livraison.strip(),
                "telephone": telephone_livraison.strip(),
                "adresse": adresse_livraison.strip(),
                "code_postal": code_postal.strip(),
                "ville": ville.strip(),
                "pays": pays,
                "mode_livraison": mode_livraison,
                "instructions": instructions_livraison.strip() if instructions_livraison else ""
            }
            
            # Créer la commande
            create_order_from_cart(cart, adresse_complete, token)


def create_order_from_cart(cart: Cart, adresse_livraison, token: str):
    """Crée une commande à partir du panier"""
    auth_service = get_auth_service()
    from services.api_client import get_api_client
    api_client = get_api_client()
    order_service = OrderService(api_client)
    
    user_info = auth_service.get_current_user()
    if not user_info:
        st.error("❌ Impossible de récupérer les informations utilisateur")
        return
    
    user_id = user_info.get('id')
    if not user_id:
        st.error("❌ Impossible de récupérer l'ID utilisateur")
        return
    
    # Préparer les lignes de commande
    lignes_commande = []
    for item in cart.items:
        ligne = {
            'produit_id': item.produit_id,
            'quantite': item.quantite,
            'prix_unitaire': item.prix_unitaire
        }
        lignes_commande.append(ligne)
    
    # Formater l'adresse de livraison
    if isinstance(adresse_livraison, dict):
        # Adresse détaillée - formater en chaîne
        adresse_formatee = f"""
{adresse_livraison['prenom']} {adresse_livraison['nom']}
{adresse_livraison['adresse']}
{adresse_livraison['code_postal']} {adresse_livraison['ville']}
{adresse_livraison['pays']}

Contact: {adresse_livraison['email']} - {adresse_livraison['telephone']}
Mode de livraison: {adresse_livraison['mode_livraison']}
"""
        if adresse_livraison.get('instructions'):
            adresse_formatee += f"Instructions: {adresse_livraison['instructions']}"
    else:
        # Adresse simple (chaîne)
        adresse_formatee = adresse_livraison
    
    # Créer la requête de commande
    order_request = CreateOrderRequest(
        utilisateur_id=user_id,
        adresse_livraison=adresse_formatee,
        statut="en_attente",
        lignes_commande=lignes_commande
    )
    
    # Afficher un spinner pendant la création
    with st.spinner("🔄 Création de votre commande..."):
        try:
            # Créer la commande
            order = order_service.create(order_request)
            
            if order:
                # Vider le panier après création de la commande
                cart_service = get_cart_service()
                cart_service.clear_cart(token)
                
                # Afficher la confirmation
                st.success("✅ Commande créée avec succès !")
                st.balloons()
                
                # Afficher les détails de la commande
                st.subheader("📦 Détails de votre commande")
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"**Numéro de commande:** #{order.id}")
                    st.markdown(f"**Date:** {order.date_commande.strftime('%d/%m/%Y %H:%M') if order.date_commande else 'N/A'}")
                    st.markdown(f"**Statut:** {order.statut.replace('_', ' ').title()}")
                    st.markdown(f"**Total:** €{order.total:.2f}")
                
                with col2:
                    st.markdown("**Adresse de livraison:**")
                    st.markdown(adresse_livraison.replace('\n', '<br>'), unsafe_allow_html=True)
                
                # Boutons d'action
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("📦 Voir mes commandes", use_container_width=True):
                        st.session_state['selected_page'] = "📦 Mes Commandes"
                        st.rerun()
                
                with col2:
                    if st.button("🛍️ Continuer mes achats", use_container_width=True):
                        st.session_state['selected_page'] = "🛍️ Produits"
                        st.rerun()
                
                with col3:
                    if st.button("🏠 Retour à l'accueil", use_container_width=True):
                        st.session_state['selected_page'] = "🏠 Accueil"
                        st.rerun()
                
            else:
                st.error("❌ Erreur lors de la création de la commande")
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la création de la commande: {str(e)}")


def show_order_confirmation(order_id: int):
    """Affiche la page de confirmation de commande"""
    st.title("✅ Commande confirmée")
    st.markdown("---")
    
    from services.api_client import get_api_client
    api_client = get_api_client()
    order_service = OrderService(api_client)
    order = order_service.get_by_id(order_id)
    
    if not order:
        st.error("❌ Commande non trouvée")
        return
    
    # Afficher les détails de la commande
    st.subheader(f"📦 Commande #{order.id}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"**Date:** {order.date_commande.strftime('%d/%m/%Y %H:%M') if order.date_commande else 'N/A'}")
        st.markdown(f"**Statut:** {order.statut.replace('_', ' ').title()}")
        st.markdown(f"**Total:** €{order.total:.2f}")
    
    with col2:
        st.markdown("**Adresse de livraison:**")
        st.markdown(order.adresse_livraison.replace('\n', '<br>'), unsafe_allow_html=True)
    
    # Articles de la commande
    if order.lignes_commande:
        st.subheader("📋 Articles commandés")
        for ligne in order.lignes_commande:
            st.markdown(f"• {ligne.quantite}x Produit #{ligne.produit_id} - €{ligne.prix_unitaire:.2f} = €{ligne.total_ligne:.2f}")
    
    # Boutons d'action
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📦 Voir mes commandes", use_container_width=True):
            st.session_state['selected_page'] = "📦 Mes Commandes"
            st.rerun()
    
    with col2:
        if st.button("🛍️ Continuer mes achats", use_container_width=True):
            st.session_state['selected_page'] = "🛍️ Produits"
            st.rerun()
    
    with col3:
        if st.button("🏠 Retour à l'accueil", use_container_width=True):
            st.session_state['selected_page'] = "🏠 Accueil"
            st.rerun()


def show_admin_orders():
    """Affiche la page de gestion des commandes pour les administrateurs"""
    
    # Initialiser les services
    from services.api_client import get_api_client
    api_client = get_api_client()
    order_service = OrderService(api_client)
    
    # Options d'action pour l'admin
    st.markdown('<h2 class="section-title">🎯 Actions</h2>', unsafe_allow_html=True)
    
    action_options = [
        "📋 Toutes les commandes",
        "🔍 Rechercher une commande",
        "📊 Commandes par statut",
        "👤 Commandes par utilisateur",
        "📈 Statistiques des commandes"
    ]
    
    action = st.selectbox(
        "Choisir une action",
        action_options,
        key="admin_order_action",
        label_visibility="collapsed"
    )
    
    if action == "📋 Toutes les commandes":
        show_all_orders_admin(order_service)
    elif action == "🔍 Rechercher une commande":
        show_order_search_admin(order_service)
    elif action == "📊 Commandes par statut":
        show_orders_by_status_admin(order_service)
    elif action == "👤 Commandes par utilisateur":
        show_orders_by_user_admin(order_service)
    elif action == "📈 Statistiques des commandes":
        show_order_stats_admin(order_service)


def show_all_orders_admin(order_service: OrderService):
    """Affiche toutes les commandes pour l'admin"""
    st.subheader("📋 Toutes les Commandes")
    
    try:
        orders = order_service.get_all()
        
        if not orders:
            st.info("Aucune commande trouvée")
            return
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filtrer par statut",
                ["Tous"] + list(set(order.statut for order in orders)),
                key="admin_status_filter"
            )
        
        with col2:
            user_filter = st.selectbox(
                "Filtrer par utilisateur",
                ["Tous"] + list(set(f"User {order.utilisateur_id}" for order in orders)),
                key="admin_user_filter"
            )
        
        with col3:
            search_term = st.text_input("Rechercher par ID", key="admin_order_search")
        
        # Appliquer les filtres
        filtered_orders = orders
        if status_filter != "Tous":
            filtered_orders = [o for o in filtered_orders if o.statut == status_filter]
        
        if user_filter != "Tous":
            user_id = int(user_filter.split(" ")[1])
            filtered_orders = [o for o in filtered_orders if o.utilisateur_id == user_id]
        
        if search_term:
            try:
                order_id = int(search_term)
                filtered_orders = [o for o in filtered_orders if o.id == order_id]
            except ValueError:
                st.warning("Veuillez entrer un ID de commande valide")
        
        # Afficher les commandes
        for order in filtered_orders:
            with st.expander(f"Commande #{order.id} - {order.statut} - User {order.utilisateur_id}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**ID:** {order.id}")
                    st.markdown(f"**Utilisateur:** {order.utilisateur_id}")
                    st.markdown(f"**Date:** {order.date_commande}")
                    st.markdown(f"**Adresse:** {order.adresse_livraison}")
                    st.markdown(f"**Total:** €{order.total:.2f}")
                    
                    # Lignes de commande
                    if order.lignes_commande:
                        st.markdown("**Articles:**")
                        for ligne in order.lignes_commande:
                            st.markdown(f"• {ligne.quantite}x Produit #{ligne.produit_id} - €{ligne.prix_unitaire:.2f}")
                
                with col2:
                    # Gestion du statut
                    st.markdown("**Gestion du statut:**")
                    
                    current_status = order.statut
                    new_status = st.selectbox(
                        "Nouveau statut",
                        ["en_attente", "validee", "expediee", "annulee"],
                        index=["en_attente", "validee", "expediee", "annulee"].index(current_status) if current_status in ["en_attente", "validee", "expediee", "annulee"] else 0,
                        key=f"status_{order.id}"
                    )
                    
                    if st.button("Mettre à jour", key=f"update_status_{order.id}"):
                        try:
                            success = order_service.update_status(order.id, new_status)
                            if success:
                                st.success(f"Statut mis à jour vers: {new_status}")
                                st.rerun()
                            else:
                                st.error("Erreur lors de la mise à jour")
                        except Exception as e:
                            st.error(f"Erreur: {str(e)}")
                    
                    # Actions rapides
                    st.markdown("**Actions:**")
                    if st.button("Voir détails", key=f"details_{order.id}"):
                        st.session_state[f"show_order_details_{order.id}"] = True
                        st.rerun()
    
    except Exception as e:
        st.error(f"Erreur lors du chargement des commandes: {str(e)}")


def show_order_search_admin(order_service: OrderService):
    """Interface de recherche de commande pour l'admin"""
    st.subheader("🔍 Rechercher une Commande")
    
    order_id = st.number_input("ID de la commande", min_value=1, key="search_order_id")
    
    if st.button("Rechercher"):
        try:
            order = order_service.get_by_id(order_id)
            if order:
                show_order_details_admin(order, order_service)
            else:
                st.error(f"Commande #{order_id} non trouvée")
        except Exception as e:
            st.error(f"Erreur lors de la recherche: {str(e)}")


def show_orders_by_status_admin(order_service: OrderService):
    """Affiche les commandes par statut pour l'admin"""
    st.subheader("📊 Commandes par Statut")
    
    status = st.selectbox(
        "Statut",
        ["en_attente", "validee", "expediee", "annulee"],
        key="status_filter_admin"
    )
    
    if st.button("Afficher"):
        try:
            orders = order_service.get_by_status(status)
            
            if not orders:
                st.info(f"Aucune commande avec le statut '{status}'")
                return
            
            st.markdown(f"**{len(orders)} commande(s) avec le statut '{status}':**")
            
            for order in orders:
                with st.expander(f"Commande #{order.id} - User {order.utilisateur_id}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**ID:** {order.id}")
                        st.markdown(f"**Utilisateur:** {order.utilisateur_id}")
                        st.markdown(f"**Date:** {order.date_commande}")
                        st.markdown(f"**Total:** €{order.total:.2f}")
                    
                    with col2:
                        new_status = st.selectbox(
                            "Changer statut",
                            ["en_attente", "validee", "expediee", "annulee"],
                            index=["en_attente", "validee", "expediee", "annulee"].index(status),
                            key=f"change_status_{order.id}"
                        )
                        
                        if st.button("Mettre à jour", key=f"update_{order.id}"):
                            try:
                                success = order_service.update_status(order.id, new_status)
                                if success:
                                    st.success("Statut mis à jour")
                                    st.rerun()
                                else:
                                    st.error("Erreur lors de la mise à jour")
                            except Exception as e:
                                st.error(f"Erreur: {str(e)}")
        
        except Exception as e:
            st.error(f"Erreur lors du chargement: {str(e)}")


def show_orders_by_user_admin(order_service: OrderService):
    """Affiche les commandes par utilisateur pour l'admin"""
    st.subheader("👤 Commandes par Utilisateur")
    
    user_id = st.number_input("ID de l'utilisateur", min_value=1, key="user_id_filter")
    
    if st.button("Afficher les commandes"):
        try:
            orders = order_service.get_by_user(user_id)
            
            if not orders:
                st.info(f"Aucune commande pour l'utilisateur {user_id}")
                return
            
            st.markdown(f"**{len(orders)} commande(s) pour l'utilisateur {user_id}:**")
            
            for order in orders:
                with st.expander(f"Commande #{order.id} - {order.statut}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**ID:** {order.id}")
                        st.markdown(f"**Statut:** {order.statut}")
                        st.markdown(f"**Date:** {order.date_commande}")
                        st.markdown(f"**Total:** €{order.total:.2f}")
                    
                    with col2:
                        new_status = st.selectbox(
                            "Changer statut",
                            ["en_attente", "validee", "expediee", "annulee"],
                            index=["en_attente", "validee", "expediee", "annulee"].index(order.statut) if order.statut in ["en_attente", "validee", "expediee", "annulee"] else 0,
                            key=f"user_status_{order.id}"
                        )
                        
                        if st.button("Mettre à jour", key=f"user_update_{order.id}"):
                            try:
                                success = order_service.update_status(order.id, new_status)
                                if success:
                                    st.success("Statut mis à jour")
                                    st.rerun()
                                else:
                                    st.error("Erreur lors de la mise à jour")
                            except Exception as e:
                                st.error(f"Erreur: {str(e)}")
        
        except Exception as e:
            st.error(f"Erreur lors du chargement: {str(e)}")


def show_order_stats_admin(order_service: OrderService):
    """Affiche les statistiques des commandes pour l'admin"""
    st.subheader("📈 Statistiques des Commandes")
    
    try:
        orders = order_service.get_all()
        
        if not orders:
            st.info("Aucune commande trouvée")
            return
        
        # Statistiques générales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total commandes", len(orders))
        
        with col2:
            total_revenue = sum(order.total for order in orders if order.total)
            st.metric("Chiffre d'affaires", f"€{total_revenue:.2f}")
        
        with col3:
            pending_orders = len([o for o in orders if o.statut == "en_attente"])
            st.metric("En attente", pending_orders)
        
        with col4:
            completed_orders = len([o for o in orders if o.statut in ["validee", "expediee"]])
            st.metric("Terminées", completed_orders)
        
        # Répartition par statut
        st.subheader("📊 Répartition par Statut")
        
        status_counts = {}
        for order in orders:
            status_counts[order.statut] = status_counts.get(order.statut, 0) + 1
        
        for status, count in status_counts.items():
            percentage = (count / len(orders)) * 100
            st.markdown(f"**{status}:** {count} commandes ({percentage:.1f}%)")
        
        # Graphique simple
        import pandas as pd
        df = pd.DataFrame(list(status_counts.items()), columns=['Statut', 'Nombre'])
        
        if not df.empty:
            st.bar_chart(df.set_index('Statut'))
    
    except Exception as e:
        st.error(f"Erreur lors du chargement des statistiques: {str(e)}")


def show_order_details_admin(order: Order, order_service: OrderService):
    """Affiche les détails d'une commande pour l'admin"""
    st.subheader(f"📋 Détails de la Commande #{order.id}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**ID:** {order.id}")
        st.markdown(f"**Utilisateur:** {order.utilisateur_id}")
        st.markdown(f"**Date:** {order.date_commande}")
        st.markdown(f"**Statut:** {order.statut}")
        st.markdown(f"**Adresse:** {order.adresse_livraison}")
        st.markdown(f"**Total:** €{order.total:.2f}")
        
        if order.lignes_commande:
            st.markdown("**Articles:**")
            for ligne in order.lignes_commande:
                st.markdown(f"• {ligne.quantite}x Produit #{ligne.produit_id} - €{ligne.prix_unitaire:.2f}")
    
    with col2:
        st.markdown("**Gestion:**")
        
        new_status = st.selectbox(
            "Nouveau statut",
            ["en_attente", "validee", "expediee", "annulee"],
            index=["en_attente", "validee", "expediee", "annulee"].index(order.statut) if order.statut in ["en_attente", "validee", "expediee", "annulee"] else 0,
            key=f"detail_status_{order.id}"
        )
        
        if st.button("Mettre à jour le statut", key=f"detail_update_{order.id}"):
            try:
                success = order_service.update_status(order.id, new_status)
                if success:
                    st.success(f"Statut mis à jour vers: {new_status}")
                    st.rerun()
                else:
                    st.error("Erreur lors de la mise à jour")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")