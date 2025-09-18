"""
Vue d'accueil moderne inspirée de l'image
"""

import streamlit as st
import random
from services.cart_service import get_cart_service
from services.auth_service import get_auth_service


def show_home():
    """Affiche la page d'accueil moderne"""
    
    # Hero section style Back Market
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%); padding: 3rem 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; font-size: 2.5rem; margin: 0 0 1rem 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">🏪 E-commerce</h1>
        <p style="color: white; font-size: 1.1rem; margin: 0; opacity: 0.9; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">Architecture MVP Moderne</p>
        <div style="margin-top: 2rem;">
            <button style="background: white; color: #00d4aa; border: none; padding: 0.8rem 1.5rem; border-radius: 6px; font-weight: 500; font-size: 1rem; cursor: pointer; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
                🚀 Découvrir nos produits
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton interactif pour découvrir les produits
    if st.button("🚀 Découvrir nos produits", type="primary", use_container_width=True):
        st.session_state['selected_page'] = "📦 Produits"
        st.rerun()
    
    # Section "Nouveaux produits" style Back Market
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <h2 style="color: #1a1a1a; margin: 0; font-size: 1.8rem; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">Nos meilleures ventes</h2>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("Voir tous les produits →", key="view_all_products"):
            st.session_state['selected_page'] = "📦 Produits"
            st.rerun()
    
    # Grille de produits modernes
    show_products_grid()
    
    # Section détails du produit sélectionné
    if 'selected_product_detail' in st.session_state:
        show_product_detail(st.session_state['selected_product_detail'])
    
    st.markdown("---")
    
    # Métriques principales style Back Market
    st.markdown('<h2 class="section-title">📊 Nos chiffres</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">1M+</div>
            <div class="metric-label">Tonnes de CO2 évitées</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">10+</div>
            <div class="metric-label">Années d'expérience</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">4.5/5</div>
            <div class="metric-label">Note moyenne</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">100%</div>
            <div class="metric-label">Reconditionné</div>
        </div>
        """, unsafe_allow_html=True)
    


def show_products_grid():
    """Affiche une grille de produits modernes"""
    
    # Données de produits style Back Market (reconditionnés)
    products = [
        {
            "id": 1,
            "name": "iPhone 13 Pro 128Go - Reconditionné",
            "price": 509.00,
            "old_price": 1199.00,
            "status": "in_stock",
            "rating": 4.3,
            "reviews": 1886,
            "image": "📱",
            "condition": "Très bon état"
        },
        {
            "id": 2,
            "name": "MacBook Air 13\" M2 256Go - Reconditionné",
            "price": 855.62,
            "old_price": 1499.00,
            "status": "in_stock",
            "rating": 4.4,
            "reviews": 423,
            "image": "💻",
            "condition": "Excellent état"
        },
        {
            "id": 3,
            "name": "MacBook Pro 13\" M2 256Go - Reconditionné",
            "price": 838.00,
            "old_price": 1619.00,
            "status": "in_stock",
            "rating": 4.3,
            "reviews": 147,
            "image": "💻",
            "condition": "Très bon état"
        },
        {
            "id": 4,
            "name": "iPad Air 5 64Go - Reconditionné",
            "price": 399.00,
            "old_price": 599.00,
            "status": "in_stock",
            "rating": 4.5,
            "reviews": 892,
            "image": "📱",
            "condition": "Bon état"
        },
        {
            "id": 5,
            "name": "Samsung Galaxy S22 128Go - Reconditionné",
            "price": 299.00,
            "old_price": 849.00,
            "status": "in_stock",
            "rating": 4.2,
            "reviews": 567,
            "image": "📱",
            "condition": "Très bon état"
        },
        {
            "id": 6,
            "name": "AirPods Pro 2ème génération - Reconditionné",
            "price": 149.00,
            "old_price": 279.00,
            "status": "in_stock",
            "rating": 4.6,
            "reviews": 1234,
            "image": "🎧",
            "condition": "Excellent état"
        }
    ]
    
    # Créer la grille de produits
    cols = st.columns(3)
    
    for i, product in enumerate(products):
        with cols[i % 3]:
            # Statut du produit
            if product["status"] == "in_stock":
                status_html = '<span class="product-status status-in-stock">✔ Disponible</span>'
            else:
                status_html = '<span class="product-status status-out-of-stock">❌ Indisponible</span>'
            
            # Étoiles de notation
            stars = "⭐" * int(product["rating"])
            
            # Calcul du pourcentage de réduction
            discount_percent = int(((product["old_price"] - product["price"]) / product["old_price"]) * 100)
            
            # Prix avec réduction
            if product["old_price"]:
                price_html = f'''
                <div style="margin-bottom: 0.5rem;">
                    <span class="product-price-old">€{product["old_price"]:.2f} neuf</span>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <span class="product-price">À partir de €{product["price"]:.2f}</span>
                </div>
                '''
            else:
                price_html = f'<span class="product-price">€{product["price"]:.2f}</span>'
            
            # Carte produit style Back Market avec composants interactifs
            with st.container():
                # En-tête de la carte avec badge de réduction
                st.markdown(f"""
                <div class="product-card">
                    <div class="discount-badge">-{discount_percent}%</div>
                    <div style="text-align: center; font-size: 2.5rem; margin-bottom: 0.75rem; background: #f8f9fa; border-radius: 6px; padding: 1rem;">{product["image"]}</div>
                    {status_html}
                    <div class="product-rating">
                        <span class="stars">{stars}</span>
                        <span class="rating-text">({product["reviews"]})</span>
                    </div>
                    <div class="product-title">{product["name"]}</div>
                    <div style="color: #8e8e93; font-size: 0.8rem; margin-bottom: 0.5rem; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">{product["condition"]}</div>
                    <div>{price_html}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Boutons interactifs
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if st.button("👁️ Voir détail", key=f"detail_{i}", use_container_width=True):
                        st.session_state['selected_product_detail'] = product
                        st.rerun()
                
                with col2:
                    if st.button("🛒 Ajouter", key=f"add_{i}", use_container_width=True):
                        # Ajouter au panier (même pour utilisateurs anonymes)
                        cart_service = get_cart_service()
                        auth_service = get_auth_service()
                        
                        # Récupérer le token si l'utilisateur est connecté
                        token = auth_service.get_access_token() if auth_service.is_authenticated() else None
                        
                        # Ajouter au panier
                        produit_id = product.get('id', 1)  # Utiliser l'ID du produit
                        result = cart_service.add_to_cart(produit_id, 1, token)
                        
                        if result['success']:
                            st.success(f"✅ {product['name']} ajouté au panier !")
                        else:
                            st.error(f"❌ Erreur: {result['message']}")


def show_product_detail(product):
    """Affiche les détails d'un produit sélectionné"""
    st.markdown("---")
    st.markdown("### 🔍 Détails du produit")
    
    # Layout en deux colonnes
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Image du produit (ou emoji par défaut)
        if product.get('image'):
            st.markdown(f"<div style='text-align: center; font-size: 4rem; margin-bottom: 1rem; background: #f8f9fa; border-radius: 8px; padding: 2rem;'>{product['image']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: center; font-size: 4rem; margin-bottom: 1rem; background: #f8f9fa; border-radius: 8px; padding: 2rem;'>📦</div>", unsafe_allow_html=True)
    
    with col2:
        # Informations du produit
        st.markdown(f"### {product['name']}")
        
        # Prix
        if product.get('old_price'):
            discount_percent = int(((product['old_price'] - product['price']) / product['old_price']) * 100)
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <span style="text-decoration: line-through; color: #8e8e93; font-size: 1.1rem;">€{product['old_price']:.2f}</span>
                <span style="color: #00d4aa; font-size: 1.5rem; font-weight: bold; margin-left: 0.5rem;">€{product['price']:.2f}</span>
                <span style="background: #ff6b6b; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-left: 0.5rem;">-{discount_percent}%</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color: #00d4aa; font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;'>€{product['price']:.2f}</div>", unsafe_allow_html=True)
        
        # Étoiles et avis
        stars = "⭐" * int(product.get('rating', 0))
        st.markdown(f"<div style='margin-bottom: 1rem;'>{stars} <span style='color: #8e8e93;'>({product.get('reviews', 0)} avis)</span></div>", unsafe_allow_html=True)
        
        # Condition
        st.markdown(f"<div style='color: #8e8e93; margin-bottom: 1rem;'>État: {product.get('condition', 'Non spécifié')}</div>", unsafe_allow_html=True)
        
        # Statut
        if product.get('status') == 'in_stock':
            st.markdown("<div style='color: #00d4aa; margin-bottom: 1rem;'>✅ En stock</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color: #ff6b6b; margin-bottom: 1rem;'>❌ Indisponible</div>", unsafe_allow_html=True)
        
        # Bouton d'ajout au panier
        if product.get('status') == 'in_stock':
            col_qty, col_btn = st.columns([1, 2])
            
            with col_qty:
                quantite = st.number_input(
                    "Quantité",
                    min_value=1,
                    max_value=10,
                    value=1,
                    key=f"detail_qty_{product.get('id', 'unknown')}",
                    label_visibility="collapsed"
                )
            
            with col_btn:
                if st.button("🛒 Ajouter au panier", key=f"detail_add_{product.get('id', 'unknown')}", use_container_width=True, type="primary"):
                    # Ajouter au panier
                    cart_service = get_cart_service()
                    auth_service = get_auth_service()
                    
                    # Récupérer le token si l'utilisateur est connecté
                    token = auth_service.get_access_token() if auth_service.is_authenticated() else None
                    
                    # Ajouter au panier (utiliser l'ID du produit ou un ID fictif)
                    produit_id = product.get('id', 1)  # ID fictif si pas d'ID
                    result = cart_service.add_to_cart(produit_id, quantite, token)
                    
                    if result['success']:
                        st.success(f"✅ {quantite}x {product['name']} ajouté au panier !")
                    else:
                        st.error(f"❌ Erreur: {result['message']}")
        else:
            st.markdown("<div style='color: #ff6b6b; padding: 1rem; background: #fff5f5; border-radius: 6px; text-align: center;'>Produit indisponible</div>", unsafe_allow_html=True)
    
    # Bouton pour fermer les détails
    if st.button("❌ Fermer les détails", key="close_details"):
        if 'selected_product_detail' in st.session_state:
            del st.session_state['selected_product_detail']
        st.rerun()