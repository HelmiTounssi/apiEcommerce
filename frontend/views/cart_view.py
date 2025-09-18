"""
Vue pour la gestion du panier
Version corrigée - Navigation par session_state
"""

import streamlit as st
from typing import Dict, Any, Optional
from services.cart_service import get_cart_service
from services.auth_service import get_auth_service
from utils.image_utils import display_product_image
from models.cart import Cart, CartItem


def show_cart_page():
    """Affiche la page du panier"""
    st.title("🛒 Mon Panier")
    st.markdown("---")
    
    auth_service = get_auth_service()
    cart_service = get_cart_service()
    
    # Récupérer le token si l'utilisateur est connecté
    token = auth_service.get_access_token() if auth_service.is_authenticated() else None
    
    # Récupérer le panier
    cart_result = cart_service.get_cart(token)
    
    if not cart_result['success']:
        st.error(f"❌ Erreur lors de la récupération du panier: {cart_result['message']}")
        return
    
    cart = cart_result.get('cart')
    
    if not cart or not cart.items:
        st.info("🛒 Votre panier est vide")
        st.markdown("Découvrez nos produits et ajoutez-les à votre panier !")
        
        # Bouton pour aller aux produits
        if st.button("🛍️ Voir les produits", type="primary"):
            st.session_state['selected_page'] = "🛍️ Produits"
            st.rerun()
        return
    
    # Afficher le panier
    st.subheader(f"📦 {cart.nombre_items} article(s) dans votre panier")
    
    # Colonnes pour l'affichage
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
    
    with col1:
        st.markdown("**Produit**")
    with col2:
        st.markdown("**Prix unitaire**")
    with col3:
        st.markdown("**Quantité**")
    with col4:
        st.markdown("**Sous-total**")
    with col5:
        st.markdown("**Actions**")
    
    st.markdown("---")
    
    # Afficher chaque item
    for item in cart.items:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            
            with col1:
                # Informations du produit
                from utils.product_utils import get_product_name, get_product_info
                nom_produit = get_product_name(item.produit, f"Produit #{item.produit_id}")
                st.markdown(f"**{nom_produit}**")
                
                # Afficher l'image avec gestion robuste des erreurs
                product_info = get_product_info(item.produit)
                image_url = product_info.get('image_url')
                display_product_image(image_url, width=80, fallback_emoji="🛒")
            
            with col2:
                st.markdown(f"€{item.prix_unitaire:.2f}")
            
            with col3:
                # Sélecteur de quantité
                new_quantity = st.number_input(
                    "Quantité",
                    min_value=0,
                    max_value=999,
                    value=item.quantite,
                    key=f"qty_{item.produit_id}",
                    label_visibility="collapsed"
                )
                
                # Mettre à jour la quantité si elle a changé
                if new_quantity != item.quantite:
                    if new_quantity == 0:
                        # Supprimer l'item
                        result = cart_service.remove_from_cart(item.produit_id, token)
                        if result['success']:
                            st.success("✅ Produit supprimé du panier")
                            st.rerun()
                        else:
                            st.error(f"❌ Erreur: {result['message']}")
                    else:
                        # Modifier la quantité
                        result = cart_service.update_quantity(item.produit_id, new_quantity, token)
                        if result['success']:
                            st.success("✅ Quantité mise à jour")
                            st.rerun()
                        else:
                            st.error(f"❌ Erreur: {result['message']}")
            
            with col4:
                st.markdown(f"€{item.sous_total:.2f}")
            
            with col5:
                # Bouton de suppression
                if st.button("🗑️", key=f"del_{item.produit_id}", help="Supprimer du panier"):
                    result = cart_service.remove_from_cart(item.produit_id, token)
                    if result['success']:
                        st.success("✅ Produit supprimé du panier")
                        st.rerun()
                    else:
                        st.error(f"❌ Erreur: {result['message']}")
            
            st.markdown("---")
    
    # Résumé du panier
    st.subheader("💰 Résumé de la commande")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Nombre d'articles:** {cart.nombre_items}")
        st.markdown(f"**Total:** €{cart.total:.2f}")
    
    with col2:
        # Boutons d'action
        if st.button("🗑️ Vider le panier", type="secondary"):
            if st.session_state.get('confirm_clear_cart', False):
                result = cart_service.clear_cart(token)
                if result['success']:
                    st.success("✅ Panier vidé")
                    st.rerun()
                else:
                    st.error(f"❌ Erreur: {result['message']}")
                st.session_state['confirm_clear_cart'] = False
            else:
                st.session_state['confirm_clear_cart'] = True
                st.warning("⚠️ Cliquez à nouveau pour confirmer")
        
        if st.session_state.get('confirm_clear_cart', False):
            st.info("⚠️ Cliquez à nouveau sur 'Vider le panier' pour confirmer")
    
    # Bouton de commande
    st.markdown("---")
    
    if auth_service.is_authenticated():
        if st.button("🛒 Passer la commande", type="primary", use_container_width=True):
            st.session_state['selected_page'] = "🛒 Finaliser la commande"
            st.rerun()
    else:
        st.info("🔐 Connectez-vous pour passer commande")
        if st.button("🔑 Se connecter", type="primary"):
            st.session_state['selected_page'] = "🔐 Connexion"
            st.rerun()


def show_cart_summary():
    """Affiche un résumé du panier dans la sidebar"""
    cart_service = get_cart_service()
    auth_service = get_auth_service()
    
    # Récupérer le token si l'utilisateur est connecté
    token = auth_service.get_access_token() if auth_service.is_authenticated() else None
    
    # Récupérer le résumé du panier
    summary_result = cart_service.get_cart_summary(token)
    
    if summary_result['success']:
        summary = summary_result['summary']
        
        if summary.nombre_items > 0:
            st.markdown("### 🛒 Panier")
            st.markdown(f"**{summary.nombre_items} article(s)**")
            st.markdown(f"**Total: €{summary.total:.2f}**")
            
            if st.button("Voir le panier", use_container_width=True):
                st.session_state['selected_page'] = "🛒 Mon Panier"
                st.rerun()
        else:
            st.markdown("### 🛒 Panier vide")


def show_add_to_cart_button(produit_id: int, produit_nom: str, prix: float, stock: int = 0):
    """Affiche un bouton d'ajout au panier pour un produit"""
    cart_service = get_cart_service()
    auth_service = get_auth_service()
    
    # Récupérer le token si l'utilisateur est connecté
    token = auth_service.get_access_token() if auth_service.is_authenticated() else None
    
    # Sélecteur de quantité
    col1, col2 = st.columns([1, 2])
    
    with col1:
        quantite = st.number_input(
            "Quantité",
            min_value=1,
            max_value=stock if stock > 0 else 999,
            value=1,
            key=f"add_qty_{produit_id}",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button(f"🛒 Ajouter au panier", key=f"add_cart_{produit_id}", use_container_width=True):
            if stock > 0 and quantite > stock:
                st.error(f"❌ Stock insuffisant. Disponible: {stock}")
            else:
                result = cart_service.add_to_cart(produit_id, quantite, token)
                if result['success']:
                    st.success(f"✅ {quantite}x {produit_nom} ajouté au panier")
                else:
                    st.error(f"❌ Erreur: {result['message']}")


def show_cart_icon():
    """Affiche l'icône du panier avec le nombre d'items"""
    cart_service = get_cart_service()
    auth_service = get_auth_service()
    
    # Récupérer le token si l'utilisateur est connecté
    token = auth_service.get_access_token() if auth_service.is_authenticated() else None
    
    # Récupérer le nombre d'items
    item_count = cart_service.get_cart_item_count(token)
    
    if item_count > 0:
        st.markdown(f"🛒 ({item_count})")
    else:
        st.markdown("🛒")
