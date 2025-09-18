"""
Utilitaires pour la gestion des images dans le frontend
"""

import streamlit as st
from typing import Optional


def display_product_image(image_url: Optional[str], width: int = 80, fallback_emoji: str = "📦") -> None:
    """
    Affiche une image de produit de manière robuste avec gestion d'erreurs
    
    Args:
        image_url: URL de l'image (complète ou relative)
        width: Largeur de l'image en pixels
        fallback_emoji: Emoji à afficher en cas d'erreur ou d'image manquante
    """
    if not image_url:
        # Pas d'URL d'image, afficher l'emoji par défaut
        st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{fallback_emoji}</div>", unsafe_allow_html=True)
        return
    
    try:
        # Vérifier si c'est une URL complète (http/https)
        if image_url.startswith(('http://', 'https://')):
            # URL complète, essayer de charger l'image
            st.image(image_url, width=width)
        else:
            # URL relative ou locale, ne pas essayer de charger avec st.image
            # Car Streamlit ne peut pas accéder aux fichiers locaux du backend
            st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{fallback_emoji}</div>", unsafe_allow_html=True)
    except Exception as e:
        # En cas d'erreur, afficher l'emoji par défaut
        print(f"Erreur lors du chargement de l'image {image_url}: {e}")
        st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{fallback_emoji}</div>", unsafe_allow_html=True)


def display_product_card_image(image_url: Optional[str], fallback_emoji: str = "📦") -> str:
    """
    Retourne le HTML pour afficher une image dans une carte produit
    
    Args:
        image_url: URL de l'image (complète ou relative)
        fallback_emoji: Emoji à afficher en cas d'erreur ou d'image manquante
    
    Returns:
        HTML string pour l'affichage de l'image
    """
    if not image_url:
        return f"<div style='font-size: 3rem; text-align: center;'>{fallback_emoji}</div>"
    
    if image_url.startswith(('http://', 'https://')):
        # URL complète, retourner une balise img HTML
        return f"<img src='{image_url}' style='width: 100%; max-width: 200px; height: auto; border-radius: 8px;' alt='Image produit' />"
    else:
        # URL relative ou locale, utiliser l'emoji par défaut
        return f"<div style='font-size: 3rem; text-align: center;'>{fallback_emoji}</div>"


def is_valid_image_url(image_url: Optional[str]) -> bool:
    """
    Vérifie si une URL d'image est valide et utilisable par Streamlit
    
    Args:
        image_url: URL à vérifier
    
    Returns:
        True si l'URL est valide et utilisable, False sinon
    """
    if not image_url:
        return False
    
    # Seules les URLs complètes sont utilisables par Streamlit
    return image_url.startswith(('http://', 'https://'))
