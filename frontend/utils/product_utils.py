"""
Utilitaires pour la gestion des produits
"""

import json
from typing import Dict, Any, Optional


def parse_product_data(produit_data: Any) -> Optional[Dict[str, Any]]:
    """
    Parse les données de produit qui peuvent être un dictionnaire ou une chaîne JSON
    
    Args:
        produit_data: Données du produit (dict, str ou None)
        
    Returns:
        Dictionnaire des données du produit ou None si parsing échoue
    """
    if produit_data is None:
        return None
    
    if isinstance(produit_data, dict):
        return produit_data
    
    if isinstance(produit_data, str):
        try:
            # Remplacer les simples quotes par des doubles quotes pour un JSON valide
            json_str = produit_data.replace("'", '"')
            # Gérer les valeurs None dans la chaîne
            json_str = json_str.replace('None', 'null')
            return json.loads(json_str)
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Erreur parsing produit: {e}")
            print(f"Chaîne originale: {produit_data}")
            return None
    
    return None


def get_product_name(produit_data: Any, default: str = "Produit") -> str:
    """
    Récupère le nom d'un produit en gérant le parsing automatique
    
    Args:
        produit_data: Données du produit (dict, str ou None)
        default: Nom par défaut si le produit n'est pas trouvé
        
    Returns:
        Nom du produit ou valeur par défaut
    """
    parsed_product = parse_product_data(produit_data)
    if parsed_product and isinstance(parsed_product, dict):
        return parsed_product.get('nom', default)
    return default


def get_product_info(produit_data: Any) -> Dict[str, Any]:
    """
    Récupère toutes les informations d'un produit en gérant le parsing automatique
    
    Args:
        produit_data: Données du produit (dict, str ou None)
        
    Returns:
        Dictionnaire avec les informations du produit
    """
    parsed_product = parse_product_data(produit_data)
    if parsed_product and isinstance(parsed_product, dict):
        return parsed_product
    return {
        'nom': 'Produit',
        'description': '',
        'prix': 0.0,
        'categorie': '',
        'image_url': None,
        'quantite_stock': 0
    }
