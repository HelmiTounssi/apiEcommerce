"""
Implémentation du service panier
"""

from typing import List, Optional, Dict, Any
from ...domain.models.panier import Panier, PanierItem
from ...data.repositories.panier_repository import PanierRepository
from ...domain.models.produit import Produit


class PanierService:
    """Implémentation du service panier"""
    
    def __init__(self):
        self.repository = PanierRepository()
    
    def get_panier_utilisateur(self, utilisateur_id: int) -> Optional[Panier]:
        """Récupère le panier d'un utilisateur"""
        return self.repository.get_ou_creer_panier_utilisateur(utilisateur_id)
    
    def get_panier_session(self, session_id: str) -> Optional[Panier]:
        """Récupère le panier d'une session"""
        return self.repository.get_ou_creer_panier_session(session_id)
    
    def ajouter_produit_utilisateur(self, utilisateur_id: int, produit_id: int, quantite: int = 1) -> Dict[str, Any]:
        """Ajoute un produit au panier d'un utilisateur"""
        try:
            # Vérifier que le produit existe et est en stock
            produit = Produit.query.get(produit_id)
            if not produit:
                return {'success': False, 'message': 'Produit non trouvé'}
            
            if produit.quantite_stock < quantite:
                return {'success': False, 'message': f'Stock insuffisant. Disponible: {produit.quantite_stock}'}
            
            # Récupérer ou créer le panier
            panier = self.repository.get_ou_creer_panier_utilisateur(utilisateur_id)
            
            # Ajouter le produit
            item = panier.ajouter_produit(produit_id, quantite)
            
            return {
                'success': True,
                'message': 'Produit ajouté au panier',
                'panier': panier.to_dict(),
                'item': item.to_dict()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de l\'ajout: {str(e)}'}
    
    def ajouter_produit_session(self, session_id: str, produit_id: int, quantite: int = 1) -> Dict[str, Any]:
        """Ajoute un produit au panier d'une session"""
        try:
            # Vérifier que le produit existe et est en stock
            produit = Produit.query.get(produit_id)
            if not produit:
                return {'success': False, 'message': 'Produit non trouvé'}
            
            if produit.quantite_stock < quantite:
                return {'success': False, 'message': f'Stock insuffisant. Disponible: {produit.quantite_stock}'}
            
            # Récupérer ou créer le panier
            panier = self.repository.get_ou_creer_panier_session(session_id)
            
            # Ajouter le produit
            item = panier.ajouter_produit(produit_id, quantite)
            
            return {
                'success': True,
                'message': 'Produit ajouté au panier',
                'panier': panier.to_dict(),
                'item': item.to_dict()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de l\'ajout: {str(e)}'}
    
    def supprimer_produit_utilisateur(self, utilisateur_id: int, produit_id: int) -> Dict[str, Any]:
        """Supprime un produit du panier d'un utilisateur"""
        try:
            panier = self.repository.get_panier_utilisateur(utilisateur_id)
            if not panier:
                return {'success': False, 'message': 'Panier non trouvé'}
            
            success = panier.supprimer_produit(produit_id)
            if success:
                return {
                    'success': True,
                    'message': 'Produit supprimé du panier',
                    'panier': panier.to_dict()
                }
            else:
                return {'success': False, 'message': 'Produit non trouvé dans le panier'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la suppression: {str(e)}'}
    
    def supprimer_produit_session(self, session_id: str, produit_id: int) -> Dict[str, Any]:
        """Supprime un produit du panier d'une session"""
        try:
            panier = self.repository.get_panier_session(session_id)
            if not panier:
                return {'success': False, 'message': 'Panier non trouvé'}
            
            success = panier.supprimer_produit(produit_id)
            if success:
                return {
                    'success': True,
                    'message': 'Produit supprimé du panier',
                    'panier': panier.to_dict()
                }
            else:
                return {'success': False, 'message': 'Produit non trouvé dans le panier'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la suppression: {str(e)}'}
    
    def modifier_quantite_utilisateur(self, utilisateur_id: int, produit_id: int, quantite: int) -> Dict[str, Any]:
        """Modifie la quantité d'un produit dans le panier d'un utilisateur"""
        try:
            panier = self.repository.get_panier_utilisateur(utilisateur_id)
            if not panier:
                return {'success': False, 'message': 'Panier non trouvé'}
            
            # Vérifier le stock si on augmente la quantité
            if quantite > 0:
                produit = Produit.query.get(produit_id)
                if not produit:
                    return {'success': False, 'message': 'Produit non trouvé'}
                
                # Trouver l'item actuel pour comparer les quantités
                item_actuel = None
                for item in panier.items:
                    if item.produit_id == produit_id:
                        item_actuel = item
                        break
                
                quantite_actuelle = item_actuel.quantite if item_actuel else 0
                difference = quantite - quantite_actuelle
                
                if difference > 0 and produit.quantite_stock < difference:
                    return {'success': False, 'message': f'Stock insuffisant. Disponible: {produit.quantite_stock}'}
            
            success = panier.modifier_quantite(produit_id, quantite)
            if success:
                return {
                    'success': True,
                    'message': 'Quantité modifiée',
                    'panier': panier.to_dict()
                }
            else:
                return {'success': False, 'message': 'Produit non trouvé dans le panier'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la modification: {str(e)}'}
    
    def modifier_quantite_session(self, session_id: str, produit_id: int, quantite: int) -> Dict[str, Any]:
        """Modifie la quantité d'un produit dans le panier d'une session"""
        try:
            panier = self.repository.get_panier_session(session_id)
            if not panier:
                return {'success': False, 'message': 'Panier non trouvé'}
            
            # Vérifier le stock si on augmente la quantité
            if quantite > 0:
                produit = Produit.query.get(produit_id)
                if not produit:
                    return {'success': False, 'message': 'Produit non trouvé'}
                
                # Trouver l'item actuel pour comparer les quantités
                item_actuel = None
                for item in panier.items:
                    if item.produit_id == produit_id:
                        item_actuel = item
                        break
                
                quantite_actuelle = item_actuel.quantite if item_actuel else 0
                difference = quantite - quantite_actuelle
                
                if difference > 0 and produit.quantite_stock < difference:
                    return {'success': False, 'message': f'Stock insuffisant. Disponible: {produit.quantite_stock}'}
            
            success = panier.modifier_quantite(produit_id, quantite)
            if success:
                return {
                    'success': True,
                    'message': 'Quantité modifiée',
                    'panier': panier.to_dict()
                }
            else:
                return {'success': False, 'message': 'Produit non trouvé dans le panier'}
                
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la modification: {str(e)}'}
    
    def vider_panier_utilisateur(self, utilisateur_id: int) -> Dict[str, Any]:
        """Vide le panier d'un utilisateur"""
        try:
            panier = self.repository.get_panier_utilisateur(utilisateur_id)
            if not panier:
                return {'success': False, 'message': 'Panier non trouvé'}
            
            panier.vider()
            return {
                'success': True,
                'message': 'Panier vidé',
                'panier': panier.to_dict()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors du vidage: {str(e)}'}
    
    def vider_panier_session(self, session_id: str) -> Dict[str, Any]:
        """Vide le panier d'une session"""
        try:
            panier = self.repository.get_panier_session(session_id)
            if not panier:
                return {'success': False, 'message': 'Panier non trouvé'}
            
            panier.vider()
            return {
                'success': True,
                'message': 'Panier vidé',
                'panier': panier.to_dict()
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors du vidage: {str(e)}'}
    
    def migrer_panier_session_vers_utilisateur(self, session_id: str, utilisateur_id: int) -> Dict[str, Any]:
        """Migre un panier de session vers un utilisateur"""
        try:
            panier = self.repository.migrer_panier_session_vers_utilisateur(session_id, utilisateur_id)
            return {
                'success': True,
                'message': 'Panier migré avec succès',
                'panier': panier.to_dict()
            }
        except Exception as e:
            return {'success': False, 'message': f'Erreur lors de la migration: {str(e)}'}
    
    def get_resume_panier_utilisateur(self, utilisateur_id: int) -> Dict[str, Any]:
        """Récupère le résumé du panier d'un utilisateur"""
        panier = self.repository.get_panier_utilisateur(utilisateur_id)
        if not panier:
            return {
                'nombre_items': 0,
                'total': 0.0,
                'items': []
            }
        
        return {
            'nombre_items': panier.calculer_nombre_items(),
            'total': panier.calculer_total(),
            'items': [item.to_dict() for item in panier.items]
        }
    
    def get_resume_panier_session(self, session_id: str) -> Dict[str, Any]:
        """Récupère le résumé du panier d'une session"""
        panier = self.repository.get_panier_session(session_id)
        if not panier:
            return {
                'nombre_items': 0,
                'total': 0.0,
                'items': []
            }
        
        return {
            'nombre_items': panier.calculer_nombre_items(),
            'total': panier.calculer_total(),
            'items': [item.to_dict() for item in panier.items]
        }
