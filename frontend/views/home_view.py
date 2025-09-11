"""
Vue d'accueil moderne inspirée de l'image
"""

import streamlit as st
from ..services.api_client import get_api_client
import random


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
    
    # Section "Nouveaux produits" style Back Market
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h2 style="color: #1a1a1a; margin: 0; font-size: 1.8rem; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 600;">Nos meilleures ventes</h2>
        <a href="#" style="color: #00d4aa; text-decoration: none; font-weight: 500; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;">Voir tous les produits →</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Grille de produits modernes
    show_products_grid()
    
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
    
    st.markdown("---")
    
    # Statut de l'API avec design moderne
    st.markdown('<h2 class="section-title">📡 Statut du système</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 4px solid #27ae60;">
            <h4 style="color: #27ae60; margin: 0 0 1rem 0;">🟢 API Backend</h4>
            <p style="margin: 0; color: #2c3e50;">Service opérationnel</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 4px solid #3498db;">
            <h4 style="color: #3498db; margin: 0 0 1rem 0;">🟢 Base de données</h4>
            <p style="margin: 0; color: #2c3e50;">Connexion active</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🔄 Vérifier la connexion API", use_container_width=True):
        try:
            api_client = get_api_client()
            response = api_client._make_request("GET", "/")
            if response:
                st.success("✅ API connectée et fonctionnelle")
            else:
                st.error("❌ API non disponible")
        except Exception as e:
            st.error(f"❌ Erreur de connexion: {str(e)}")
    
    st.markdown("---")
    
    # Architecture avec design moderne
    st.markdown('<h2 class="section-title">🏗️ Architecture</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h4 style="color: #2c3e50; margin: 0 0 1rem 0;">🔧 Backend (Couches)</h4>
            <ul style="color: #2c3e50; margin: 0;">
                <li><strong>Domain:</strong> Entités métier</li>
                <li><strong>Data:</strong> Repositories</li>
                <li><strong>Service:</strong> Logique métier</li>
                <li><strong>Controller:</strong> API REST</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <h4 style="color: #2c3e50; margin: 0 0 1rem 0;">🎨 Frontend (MVP)</h4>
            <ul style="color: #2c3e50; margin: 0;">
                <li><strong>Models:</strong> Structures de données</li>
                <li><strong>Services:</strong> Appels API</li>
                <li><strong>Presenters:</strong> Logique présentation</li>
                <li><strong>Views:</strong> Interface Streamlit</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def show_products_grid():
    """Affiche une grille de produits modernes"""
    
    # Données de produits style Back Market (reconditionnés)
    products = [
        {
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
            
            # Carte produit style Back Market
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
                <button class="btn-primary" style="width: 100%; margin-top: 0.75rem;">Voir l'offre</button>
            </div>
            """, unsafe_allow_html=True)