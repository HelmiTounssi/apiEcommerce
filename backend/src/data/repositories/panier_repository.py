"""
Repository pour la gestion du panier
"""

from typing import List, Optional
from .base_repository import BaseRepository
from ...domain.models.panier import Panier, PanierItem
from ...data.database.db import db


class PanierRepository(BaseRepository):
    """Repository pour la gestion du panier"""
    
    def __init__(self):
        super().__init__(Panier)
    
    def get_panier_utilisateur(self, utilisateur_id: int) -> Optional[Panier]:
        """Récupère le panier actif d'un utilisateur"""
        return Panier.query.filter_by(
            utilisateur_id=utilisateur_id,
            statut='actif'
        ).first()
    
    def get_panier_session(self, session_id: str) -> Optional[Panier]:
        """Récupère le panier d'une session"""
        return Panier.query.filter_by(
            session_id=session_id,
            statut='actif'
        ).first()
    
    def creer_panier_utilisateur(self, utilisateur_id: int) -> Panier:
        """Crée un nouveau panier pour un utilisateur"""
        panier = Panier(
            utilisateur_id=utilisateur_id,
            statut='actif'
        )
        db.session.add(panier)
        db.session.commit()
        return panier
    
    def creer_panier_session(self, session_id: str) -> Panier:
        """Crée un nouveau panier pour une session"""
        panier = Panier(
            utilisateur_id=None,  # Explicitement None pour les utilisateurs anonymes
            session_id=session_id,
            statut='actif'
        )
        db.session.add(panier)
        db.session.commit()
        return panier
    
    def get_ou_creer_panier_utilisateur(self, utilisateur_id: int) -> Panier:
        """Récupère ou crée un panier pour un utilisateur"""
        panier = self.get_panier_utilisateur(utilisateur_id)
        if not panier:
            panier = self.creer_panier_utilisateur(utilisateur_id)
        return panier
    
    def get_ou_creer_panier_session(self, session_id: str) -> Panier:
        """Récupère ou crée un panier pour une session"""
        panier = self.get_panier_session(session_id)
        if not panier:
            panier = self.creer_panier_session(session_id)
        return panier
    
    def migrer_panier_session_vers_utilisateur(self, session_id: str, utilisateur_id: int) -> Panier:
        """Migre un panier de session vers un utilisateur"""
        panier_session = self.get_panier_session(session_id)
        panier_utilisateur = self.get_panier_utilisateur(utilisateur_id)
        
        if panier_session and not panier_utilisateur:
            # Migrer le panier de session vers l'utilisateur
            panier_session.utilisateur_id = utilisateur_id
            panier_session.session_id = None
            db.session.commit()
            return panier_session
        elif panier_session and panier_utilisateur:
            # Fusionner les paniers
            for item in panier_session.items:
                item_existant = PanierItem.query.filter_by(
                    panier_id=panier_utilisateur.id,
                    produit_id=item.produit_id
                ).first()
                
                if item_existant:
                    item_existant.quantite += item.quantite
                else:
                    item.panier_id = panier_utilisateur.id
                    db.session.add(item)
            
            # Supprimer le panier de session
            db.session.delete(panier_session)
            db.session.commit()
            return panier_utilisateur
        elif panier_utilisateur:
            return panier_utilisateur
        else:
            return self.creer_panier_utilisateur(utilisateur_id)
    
    def abandonner_panier(self, panier_id: int) -> bool:
        """Marque un panier comme abandonné"""
        panier = self.get_by_id(panier_id)
        if panier:
            panier.statut = 'abandonne'
            db.session.commit()
            return True
        return False
    
    def convertir_panier_en_commande(self, panier_id: int) -> bool:
        """Marque un panier comme converti en commande"""
        panier = self.get_by_id(panier_id)
        if panier:
            panier.statut = 'converti'
            db.session.commit()
            return True
        return False
    
    def get_paniers_abandonnes(self, jours: int = 7) -> List[Panier]:
        """Récupère les paniers abandonnés depuis X jours"""
        from datetime import datetime, timedelta
        date_limite = datetime.utcnow() - timedelta(days=jours)
        
        return Panier.query.filter(
            Panier.statut == 'abandonne',
            Panier.date_modification < date_limite
        ).all()
    
    def nettoyer_paniers_abandonnes(self, jours: int = 30) -> int:
        """Nettoie les paniers abandonnés anciens"""
        paniers_abandonnes = self.get_paniers_abandonnes(jours)
        count = len(paniers_abandonnes)
        
        for panier in paniers_abandonnes:
            db.session.delete(panier)
        
        db.session.commit()
        return count
