"""
Vue pour la gestion des produits
"""

import streamlit as st
from ..services.api_client import get_api_client
from ..services import ProductService
from ..services.auth_service import get_auth_service
from ..presenters import ProductPresenter


def show_products():
    """Affiche la page de gestion des produits"""
    
    # Vérifier l'authentification et le rôle
    auth_service = get_auth_service()
    is_authenticated = auth_service.is_authenticated()
    is_admin = auth_service.is_admin() if is_authenticated else False
    
    # Header style Back Market adapté selon le rôle
    if is_admin:
        title = "📦 Gestion des Produits"
        subtitle = "Administration - Catalogue et inventaire"
    elif is_authenticated:
        title = "📦 Catalogue Produits"
        subtitle = "Découvrez notre sélection de produits"
    else:
        title = "📦 Catalogue Produits"
        subtitle = "Découvrez notre sélection de produits"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; font-size: 2.2rem; margin: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">{title}</h1>
        <p style="color: white; font-size: 1rem; margin: 0; opacity: 0.9; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialiser les services
    api_client = get_api_client()
    product_service = ProductService(api_client)
    product_presenter = ProductPresenter(product_service)
    
    # Menu des actions adapté selon le rôle
    st.markdown('<h2 class="section-title">🎯 Actions</h2>', unsafe_allow_html=True)
    
    if is_admin:
        # Options pour les administrateurs
        action_options = [
            "📋 Liste des produits",
            "➕ Créer un produit", 
            "✏️ Modifier un produit",
            "🗑️ Supprimer un produit",
            "📦 Gestion des stocks",
            "🔍 Rechercher un produit",
            "📊 Statistiques"
        ]
    else:
        # Options pour les visiteurs et clients
        action_options = [
            "📋 Parcourir le catalogue",
            "🔍 Rechercher un produit",
            "📊 Statistiques du catalogue"
        ]
    
    action = st.selectbox(
        "Choisir une action",
        action_options,
        key="product_action",
        label_visibility="collapsed"
    )
    
    # Routage des actions selon le rôle
    if action == "📋 Liste des produits" or action == "📋 Parcourir le catalogue":
        show_product_catalog(product_presenter, is_admin)
    
    elif action == "➕ Créer un produit":
        if is_admin:
            product_presenter.show_create_form()
        else:
            st.error("🔒 Cette fonctionnalité est réservée aux administrateurs.")
    
    elif action == "✏️ Modifier un produit":
        if is_admin:
            show_product_edit_form(product_presenter)
        else:
            st.error("🔒 Cette fonctionnalité est réservée aux administrateurs.")
    
    elif action == "🗑️ Supprimer un produit":
        if is_admin:
            show_product_delete_form(product_presenter)
        else:
            st.error("🔒 Cette fonctionnalité est réservée aux administrateurs.")
    
    elif action == "📦 Gestion des stocks":
        if is_admin:
            show_stock_management(product_presenter)
        else:
            st.error("🔒 Cette fonctionnalité est réservée aux administrateurs.")
    
    elif action == "🔍 Rechercher un produit":
        show_product_search(product_presenter)
    
    elif action == "📊 Statistiques" or action == "📊 Statistiques du catalogue":
        show_product_analytics(product_presenter)
    
    # Gestion des actions contextuelles
    handle_product_actions(product_presenter)
    
    # Gestion de l'affichage des détails de produit
    handle_product_detail_display(product_presenter)
    
    # Debug: afficher l'état de l'authentification
    if is_admin:
        show_auth_debug_info()


def show_product_catalog(product_presenter: ProductPresenter, is_admin: bool):
    """Affiche le catalogue des produits avec interface adaptée selon le rôle"""
    
    if is_admin:
        st.subheader("📋 Liste des Produits - Administration")
        product_presenter.show_list()
    else:
        st.subheader("📋 Catalogue des Produits")
        show_catalog_grid(product_presenter)


def show_catalog_grid(product_presenter: ProductPresenter):
    """Affiche le catalogue sous forme de grille pour les visiteurs/clients"""
    
    # Charger tous les produits
    products = product_presenter.service.get_all()
    
    if not products:
        st.info("ℹ️ Aucun produit disponible dans le catalogue")
        return
    
    # Filtres pour le catalogue
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filtre par catégorie
        categories = ["Toutes"] + list(set(p.categorie for p in products))
        selected_category = st.selectbox("Filtrer par catégorie", categories)
    
    with col2:
        # Filtre par disponibilité
        availability = st.selectbox("Disponibilité", ["Tous", "En stock", "Rupture de stock"])
    
    with col3:
        # Tri
        sort_option = st.selectbox("Trier par", ["Nom", "Prix croissant", "Prix décroissant", "Stock"])
    
    # Appliquer les filtres
    filtered_products = products
    
    if selected_category != "Toutes":
        filtered_products = [p for p in filtered_products if p.categorie == selected_category]
    
    if availability == "En stock":
        filtered_products = [p for p in filtered_products if p.quantite_stock > 0]
    elif availability == "Rupture de stock":
        filtered_products = [p for p in filtered_products if p.quantite_stock == 0]
    
    # Appliquer le tri
    if sort_option == "Nom":
        filtered_products.sort(key=lambda x: x.nom)
    elif sort_option == "Prix croissant":
        filtered_products.sort(key=lambda x: x.prix)
    elif sort_option == "Prix décroissant":
        filtered_products.sort(key=lambda x: x.prix, reverse=True)
    elif sort_option == "Stock":
        filtered_products.sort(key=lambda x: x.quantite_stock, reverse=True)
    
    st.write(f"**{len(filtered_products)} produit(s) trouvé(s)**")
    
    # Affichage en grille
    cols_per_row = 3
    for i in range(0, len(filtered_products), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            if i + j < len(filtered_products):
                product = filtered_products[i + j]
                
                with col:
                    # Carte produit
                    st.markdown(f"""
                    <div style="
                        border: 1px solid #e0e0e0;
                        border-radius: 12px;
                        padding: 1rem;
                        margin-bottom: 1rem;
                        background: white;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        transition: transform 0.2s;
                    ">
                        <h4 style="margin: 0 0 0.5rem 0; color: #333;">{product.nom}</h4>
                        <p style="margin: 0 0 0.5rem 0; color: #666; font-size: 0.9rem;">{product.categorie}</p>
                        <p style="margin: 0 0 0.5rem 0; color: #00d4aa; font-weight: bold; font-size: 1.2rem;">{product.prix:.2f} €</p>
                        <p style="margin: 0; color: {'#28a745' if product.quantite_stock > 0 else '#dc3545'}; font-size: 0.9rem;">
                            {'✅ En stock' if product.quantite_stock > 0 else '❌ Rupture'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Bouton pour voir les détails
                    if st.button(f"Voir détails", key=f"view_product_{product.id}"):
                        st.session_state[f"show_product_detail_{product.id}"] = True
                        st.rerun()


def show_product_edit_form(product_presenter: ProductPresenter):
    """Affiche le formulaire de modification de produit pour les admins"""
    st.subheader("✏️ Modifier un Produit")
    
    # Sélection du produit à modifier
    products = product_presenter.service.get_all()
    
    if not products:
        st.info("Aucun produit à modifier")
        return
    
    product_options = {f"{p.nom} (ID: {p.id})": p.id for p in products}
    selected_product_name = st.selectbox("Sélectionner le produit à modifier", list(product_options.keys()))
    
    if selected_product_name:
        product_id = product_options[selected_product_name]
        
        if st.button("Modifier ce produit"):
            st.session_state[f"edit_product_{product_id}"] = True
            st.rerun()


def show_product_delete_form(product_presenter: ProductPresenter):
    """Affiche le formulaire de suppression de produit pour les admins"""
    st.subheader("🗑️ Supprimer un Produit")
    
    # Sélection du produit à supprimer
    products = product_presenter.service.get_all()
    
    if not products:
        st.info("Aucun produit à supprimer")
        return
    
    product_options = {f"{p.nom} (ID: {p.id})": p.id for p in products}
    selected_product_name = st.selectbox("Sélectionner le produit à supprimer", list(product_options.keys()))
    
    if selected_product_name:
        product_id = product_options[selected_product_name]
        
        # Afficher les détails du produit avant suppression
        product = next((p for p in products if p.id == product_id), None)
        if product:
            st.warning("⚠️ **Produit sélectionné pour suppression :**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Nom :** {product.nom}")
                st.write(f"**Catégorie :** {product.categorie}")
                st.write(f"**Prix :** {product.prix:.2f} €")
            
            with col2:
                st.write(f"**Stock :** {product.quantite_stock}")
                st.write(f"**Description :** {product.description[:100]}...")
            
            # Confirmation de suppression
            if st.button("🗑️ Confirmer la suppression", type="primary"):
                if product_presenter.service.delete(product_id):
                    st.success("✅ Produit supprimé avec succès")
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la suppression")


def show_stock_management(product_presenter: ProductPresenter):
    """Affiche la gestion des stocks pour les admins"""
    st.subheader("📦 Gestion des Stocks")
    
    # Charger tous les produits
    products = product_presenter.service.get_all()
    
    if not products:
        st.info("Aucun produit à gérer")
        return
    
    # Filtres pour la gestion des stocks
    col1, col2 = st.columns(2)
    
    with col1:
        stock_filter = st.selectbox("Filtrer par état du stock", 
                                  ["Tous", "En stock", "Stock faible (≤5)", "Rupture de stock"])
    
    with col2:
        category_filter = st.selectbox("Filtrer par catégorie", 
                                     ["Toutes"] + list(set(p.categorie for p in products)))
    
    # Appliquer les filtres
    filtered_products = products
    
    if stock_filter == "En stock":
        filtered_products = [p for p in filtered_products if p.quantite_stock > 5]
    elif stock_filter == "Stock faible (≤5)":
        filtered_products = [p for p in filtered_products if 0 < p.quantite_stock <= 5]
    elif stock_filter == "Rupture de stock":
        filtered_products = [p for p in filtered_products if p.quantite_stock == 0]
    
    if category_filter != "Toutes":
        filtered_products = [p for p in filtered_products if p.categorie == category_filter]
    
    st.write(f"**{len(filtered_products)} produit(s) trouvé(s)**")
    
    # Affichage des produits avec gestion de stock
    for product in filtered_products:
        with st.expander(f"{product.nom} - Stock: {product.quantite_stock}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Catégorie :** {product.categorie}")
                st.write(f"**Prix :** {product.prix:.2f} €")
            
            with col2:
                st.write(f"**Stock actuel :** {product.quantite_stock}")
                
                # Indicateur de stock
                if product.quantite_stock == 0:
                    st.error("❌ Rupture de stock")
                elif product.quantite_stock <= 5:
                    st.warning("⚠️ Stock faible")
                else:
                    st.success("✅ Stock suffisant")
            
            with col3:
                # Modification du stock
                new_stock = st.number_input(
                    "Nouveau stock",
                    min_value=0,
                    value=product.quantite_stock,
                    key=f"stock_{product.id}"
                )
                
                if st.button("Mettre à jour", key=f"update_stock_{product.id}"):
                    # Mettre à jour le stock
                    updated_product = product
                    updated_product.quantite_stock = new_stock
                    
                    if product_presenter.service.update(product.id, updated_product):
                        st.success("✅ Stock mis à jour")
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la mise à jour")


def show_product_search(product_presenter: ProductPresenter):
    """Affiche la recherche de produit"""
    st.subheader("🔍 Rechercher un Produit")
    
    search_type = st.radio(
        "Type de recherche",
        ["Par ID", "Par nom", "Par catégorie"],
        key="product_search_type"
    )
    
    if search_type == "Par ID":
        product_id = st.number_input("ID du produit", min_value=1, key="product_id_search")
        if st.button("Rechercher", key="search_by_id"):
            if product_id:
                product_presenter.show_detail(product_id)
            else:
                st.error("Veuillez entrer un ID valide")
    
    elif search_type == "Par nom":
        product_name = st.text_input("Nom du produit", key="product_name_search")
        if st.button("Rechercher", key="search_by_name"):
            if product_name:
                products = product_presenter.service.get_all()
                matching_products = [
                    p for p in products 
                    if product_name.lower() in p.nom.lower()
                ]
                
                if matching_products:
                    st.write(f"**{len(matching_products)} produit(s) trouvé(s):**")
                    for product in matching_products:
                        if st.button(f"{product.nom} (ID: {product.id})", key=f"select_product_{product.id}"):
                            product_presenter.show_detail(product.id)
                else:
                    st.error("Aucun produit trouvé")
            else:
                st.error("Veuillez entrer un nom valide")
    
    else:  # Par catégorie
        products = product_presenter.service.get_all()
        categories = list(set(p.categorie for p in products))
        
        if categories:
            selected_category = st.selectbox("Catégorie", categories, key="product_category_search")
            if st.button("Rechercher", key="search_by_category"):
                category_products = product_presenter.service.get_by_category(selected_category)
                
                if category_products:
                    st.write(f"**{len(category_products)} produit(s) dans la catégorie '{selected_category}':**")
                    for product in category_products:
                        if st.button(f"{product.nom} (ID: {product.id})", key=f"select_category_product_{product.id}"):
                            product_presenter.show_detail(product.id)
                else:
                    st.error("Aucun produit trouvé dans cette catégorie")
        else:
            st.info("Aucune catégorie disponible")


def show_product_analytics(product_presenter: ProductPresenter):
    """Affiche les analyses des produits"""
    st.subheader("📊 Analyses des Produits")
    
    # Statistiques générales
    stats = product_presenter.service.get_statistics()
    
    if stats["total"] > 0:
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Produits", stats["total"])
        with col2:
            st.metric("En Stock", stats["in_stock"])
        with col3:
            st.metric("Rupture", stats["out_of_stock"])
        with col4:
            st.metric("Valeur Stock", f"{stats['total_value']:.2f}€")
        
        # Analyses détaillées
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Répartition par Catégorie")
            if stats["categories"]:
                import plotly.express as px
                fig = px.pie(
                    values=list(stats["categories"].values()),
                    names=list(stats["categories"].keys()),
                    title="Produits par catégorie"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 État du Stock")
            import plotly.express as px
            stock_data = {
                "État": ["En stock", "Rupture"],
                "Nombre": [stats["in_stock"], stats["out_of_stock"]]
            }
            fig = px.bar(
                x=stock_data["État"],
                y=stock_data["Nombre"],
                title="Répartition du stock"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top produits par valeur
        st.subheader("💰 Top Produits par Valeur")
        products = stats["products"]
        if products:
            product_values = [
                {
                    "Produit": p.nom,
                    "Prix": p.prix,
                    "Stock": p.quantite_stock,
                    "Valeur": p.prix * p.quantite_stock
                }
                for p in products
            ]
            
            # Trier par valeur
            product_values.sort(key=lambda x: x["Valeur"], reverse=True)
            
            import pandas as pd
            df = pd.DataFrame(product_values[:10])  # Top 10
            st.dataframe(df, use_container_width=True)
    
    else:
        st.info("Aucune donnée disponible pour les analyses")


def handle_product_actions(product_presenter: ProductPresenter):
    """Gère les actions contextuelles sur les produits"""
    
    # Vérifier les actions d'édition
    for key, value in st.session_state.items():
        if key.startswith("edit_product_") and value:
            product_id = int(key.split("_")[2])
            product_presenter.show_update_form(product_id)
            break
    
    # Vérifier les actions de gestion du stock
    for key, value in st.session_state.items():
        if key.startswith("manage_stock_") and value:
            product_id = int(key.split("_")[2])
            product_presenter.show_stock_management(product_id)
            break


def handle_product_detail_display(product_presenter: ProductPresenter):
    """Gère l'affichage des détails de produit"""
    
    # Vérifier les demandes d'affichage de détails
    for key, value in st.session_state.items():
        if key.startswith("show_product_detail_") and value:
            product_id = int(key.split("_")[3])
            show_product_detail(product_presenter, product_id)
            break


def show_product_detail(product_presenter: ProductPresenter, product_id: int):
    """Affiche les détails d'un produit avec une interface moderne"""
    
    # Récupérer le produit
    product = product_presenter.service.get_by_id(product_id)
    
    if not product:
        st.error("❌ Produit non trouvé")
        return
    
    # Header avec bouton de retour
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("← Retour", key="back_to_catalog"):
            # Nettoyer l'état de session
            for key in list(st.session_state.keys()):
                if key.startswith("show_product_detail_"):
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        st.markdown(f"### {product.nom}")
    
    # Affichage des détails en deux colonnes
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Informations principales
        st.markdown("""
        <div style="
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        ">
        """, unsafe_allow_html=True)
        
        st.markdown(f"**📦 Catégorie :** {product.categorie}")
        st.markdown(f"**💰 Prix :** {product.prix:.2f} €")
        
        # Indicateur de disponibilité
        if product.quantite_stock > 0:
            st.markdown(f"**✅ Disponibilité :** En stock ({product.quantite_stock} unités)")
        else:
            st.markdown("**❌ Disponibilité :** Rupture de stock")
        
        st.markdown("---")
        
        # Description
        st.markdown("**📝 Description :**")
        st.write(product.description)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Actions et informations complémentaires
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #00d4aa;
        ">
        """, unsafe_allow_html=True)
        
        # Informations techniques
        st.markdown("**ℹ️ Informations :**")
        st.write(f"**ID :** {product.id}")
        st.write(f"**Date d'ajout :** {product.date_creation}")
        
        # Actions selon le rôle
        auth_service = get_auth_service()
        is_admin = auth_service.is_authenticated() and auth_service.is_admin()
        
        if is_admin:
            st.markdown("**⚙️ Actions Admin :**")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("✏️ Modifier", key=f"edit_detail_{product.id}"):
                    st.session_state[f"edit_product_{product.id}"] = True
                    st.rerun()
            
            with col_btn2:
                if st.button("🗑️ Supprimer", key=f"delete_detail_{product.id}"):
                    st.session_state[f"delete_product_{product.id}"] = True
                    st.rerun()
            
            # Gestion rapide du stock
            st.markdown("**📦 Gestion du stock :**")
            new_stock = st.number_input(
                "Stock",
                min_value=0,
                value=product.quantite_stock,
                key=f"quick_stock_{product.id}"
            )
            
            if st.button("Mettre à jour", key=f"quick_update_{product.id}"):
                updated_product = product
                updated_product.quantite_stock = new_stock
                
                if product_presenter.service.update(product.id, updated_product):
                    st.success("✅ Stock mis à jour")
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la mise à jour")
        
        else:
            # Actions pour les clients/visiteurs
            if auth_service.is_authenticated():
                st.markdown("**🛒 Actions :**")
                
                if product.quantite_stock > 0:
                    if st.button("🛒 Ajouter au panier", key=f"add_to_cart_{product.id}"):
                        st.info("🚧 Fonctionnalité de panier en cours de développement")
                else:
                    st.info("❌ Produit indisponible")
            else:
                st.info("🔒 Connectez-vous pour ajouter au panier")
        
        st.markdown("</div>", unsafe_allow_html=True)


def show_auth_debug_info():
    """Affiche les informations de debug pour l'authentification (Admin uniquement)"""
    
    with st.expander("🔧 Debug - État de l'authentification", expanded=False):
        api_client = get_api_client()
        auth_info = api_client.get_auth_info()
        
        st.write("**État de l'authentification :**")
        st.write(f"- Authentifié : {auth_info['is_authenticated']}")
        st.write(f"- Token présent : {auth_info['has_token']}")
        st.write(f"- Token (preview) : {auth_info['token_preview']}")
        
        if auth_info['user']:
            st.write(f"- Utilisateur : {auth_info['user'].get('nom', 'N/A')}")
            st.write(f"- Email : {auth_info['user'].get('email', 'N/A')}")
            st.write(f"- Rôle : {auth_info['user'].get('role', 'N/A')}")
        
        # Bouton pour tester une requête API
        if st.button("🧪 Tester une requête API authentifiée"):
            try:
                # Tester une requête simple
                response = api_client._make_request("GET", "/api/produits/")
                if response is not None:
                    st.success("✅ Requête API réussie")
                else:
                    st.error("❌ Requête API échouée")
            except Exception as e:
                st.error(f"❌ Erreur lors du test : {str(e)}")
        
        # Bouton pour rafraîchir l'état
        if st.button("🔄 Rafraîchir l'état"):
            st.rerun()
