"""
Présentateur pour la gestion des commandes
"""

import streamlit as st
from typing import List, Optional, Dict, Any
from .base_presenter import BasePresenter
from ..services import OrderService
from ..models import Order, CreateOrderRequest, UpdateOrderRequest


class OrderPresenter(BasePresenter):
    """Présentateur pour la gestion des commandes"""
    
    def __init__(self, order_service: OrderService):
        super().__init__(order_service)
        self._orders: List[Order] = []
        self._selected_order: Optional[Order] = None
        self._filter_status: str = "tous"
        self._filter_user_id: Optional[int] = None
    
    def load_orders(self) -> bool:
        """Charge la liste des commandes"""
        try:
            self._orders = self.service.get_all()
            return True
        except Exception as e:
            self.handle_error(e, "chargement des commandes")
            return False
    
    def load_orders_by_user(self, user_id: int) -> bool:
        """Charge les commandes d'un utilisateur"""
        try:
            self._orders = self.service.get_orders_by_user(user_id)
            self._filter_user_id = user_id
            return True
        except Exception as e:
            self.handle_error(e, f"chargement des commandes de l'utilisateur {user_id}")
            return False
    
    def load_orders_by_status(self, status: str) -> bool:
        """Charge les commandes par statut"""
        try:
            self._orders = self.service.get_orders_by_status(status)
            self._filter_status = status
            return True
        except Exception as e:
            self.handle_error(e, f"chargement des commandes avec statut {status}")
            return False
    
    def get_orders(self) -> List[Order]:
        """Retourne la liste des commandes"""
        return self._orders
    
    def get_filtered_orders(self) -> List[Order]:
        """Retourne les commandes filtrées"""
        filtered = self._orders
        
        if self._filter_status != "tous":
            filtered = [order for order in filtered if order.statut == self._filter_status]
        
        if self._filter_user_id is not None:
            filtered = [order for order in filtered if order.utilisateur_id == self._filter_user_id]
        
        return filtered
    
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Récupère une commande par ID"""
        try:
            return self.service.get_by_id(order_id)
        except Exception as e:
            self.handle_error(e, f"récupération de la commande {order_id}")
            return None
    
    def create_order(self, order_request: CreateOrderRequest) -> Optional[Order]:
        """Crée une nouvelle commande"""
        try:
            new_order = self.service.create(order_request)
            if new_order:
                self._orders.append(new_order)
                self.show_success(f"Commande {new_order.id} créée avec succès")
            return new_order
        except Exception as e:
            self.handle_error(e, "création de la commande")
            return None
    
    def update_order(self, order_id: int, order_request: UpdateOrderRequest) -> Optional[Order]:
        """Met à jour une commande"""
        try:
            updated_order = self.service.update(order_id, order_request)
            if updated_order:
                # Mettre à jour la liste locale
                for i, order in enumerate(self._orders):
                    if order.id == order_id:
                        self._orders[i] = updated_order
                        break
                self.show_success(f"Commande {order_id} mise à jour avec succès")
            return updated_order
        except Exception as e:
            self.handle_error(e, f"mise à jour de la commande {order_id}")
            return None
    
    def delete_order(self, order_id: int) -> bool:
        """Supprime une commande"""
        try:
            success = self.service.delete(order_id)
            if success:
                self._orders = [order for order in self._orders if order.id != order_id]
                self.show_success(f"Commande {order_id} supprimée avec succès")
            return success
        except Exception as e:
            self.handle_error(e, f"suppression de la commande {order_id}")
            return False
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Met à jour le statut d'une commande"""
        try:
            success = self.service.update_order_status(order_id, status)
            if success:
                # Mettre à jour la liste locale
                for order in self._orders:
                    if order.id == order_id:
                        order.statut = status
                        break
                self.show_success(f"Statut de la commande {order_id} mis à jour vers '{status}'")
            return success
        except Exception as e:
            self.handle_error(e, f"mise à jour du statut de la commande {order_id}")
            return False
    
    def get_order_total(self, order_id: int) -> Optional[float]:
        """Récupère le total d'une commande"""
        try:
            return self.service.get_order_total(order_id)
        except Exception as e:
            self.handle_error(e, f"calcul du total de la commande {order_id}")
            return None
    
    def get_orders_summary(self) -> Dict[str, Any]:
        """Retourne un résumé des commandes"""
        if not self._orders:
            return {
                "total_orders": 0,
                "by_status": {},
                "total_value": 0.0,
                "average_value": 0.0
            }
        
        by_status = {}
        total_value = 0.0
        
        for order in self._orders:
            # Compter par statut
            status = order.statut or "inconnu"
            by_status[status] = by_status.get(status, 0) + 1
            
            # Calculer la valeur totale
            if hasattr(order, 'total') and order.total:
                total_value += order.total
        
        return {
            "total_orders": len(self._orders),
            "by_status": by_status,
            "total_value": total_value,
            "average_value": total_value / len(self._orders) if self._orders else 0.0
        }
    
    def set_filter_status(self, status: str):
        """Définit le filtre par statut"""
        self._filter_status = status
    
    def set_filter_user(self, user_id: Optional[int]):
        """Définit le filtre par utilisateur"""
        self._filter_user_id = user_id
    
    def clear_filters(self):
        """Efface tous les filtres"""
        self._filter_status = "tous"
        self._filter_user_id = None
    
    def get_available_statuses(self) -> List[str]:
        """Retourne la liste des statuts disponibles"""
        return ["en_attente", "validée", "expédiée", "annulée"]
    
    def get_status_display_name(self, status: str) -> str:
        """Retourne le nom d'affichage d'un statut"""
        status_names = {
            "en_attente": "En attente",
            "validée": "Validée",
            "expédiée": "Expédiée",
            "annulée": "Annulée"
        }
        return status_names.get(status, status.title())
    
    def get_status_color(self, status: str) -> str:
        """Retourne la couleur d'un statut"""
        status_colors = {
            "en_attente": "🟡",
            "validée": "🟢",
            "expédiée": "🔵",
            "annulée": "🔴"
        }
        return status_colors.get(status, "⚪")
    
    # Implémentation des méthodes abstraites de BasePresenter
    def show_list(self):
        """Affiche la liste des commandes"""
        orders = self.get_filtered_orders()
        if not orders:
            self.show_info("Aucune commande trouvée")
            return
        
        for order in orders:
            with st.expander(f"Commande #{order.id} - {self.get_status_color(order.statut)} {self.get_status_display_name(order.statut)}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Utilisateur ID:** {order.utilisateur_id}")
                    st.write(f"**Date:** {order.date_commande}")
                
                with col2:
                    st.write(f"**Statut:** {self.get_status_display_name(order.statut)}")
                    st.write(f"**Adresse:** {order.adresse_livraison}")
                
                with col3:
                    if hasattr(order, 'total') and order.total:
                        st.write(f"**Total:** {order.total:.2f} €")
    
    def show_detail(self, order_id: int):
        """Affiche le détail d'une commande"""
        order = self.get_order_by_id(order_id)
        if not order:
            self.show_error(f"Commande {order_id} non trouvée")
            return
        
        st.subheader(f"📋 Détail de la Commande #{order.id}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**ID:** {order.id}")
            st.write(f"**Utilisateur ID:** {order.utilisateur_id}")
            st.write(f"**Date de création:** {order.date_commande}")
        
        with col2:
            st.write(f"**Statut:** {self.get_status_color(order.statut)} {self.get_status_display_name(order.statut)}")
            st.write(f"**Adresse de livraison:** {order.adresse_livraison}")
            if hasattr(order, 'total') and order.total:
                st.write(f"**Total:** {order.total:.2f} €")
        
        # Afficher les lignes de commande si disponibles
        if hasattr(order, 'lignes_commande') and order.lignes_commande:
            st.subheader("📦 Lignes de commande")
            for ligne in order.lignes_commande:
                st.write(f"- Produit {ligne.produit_id}: {ligne.quantite} x {ligne.prix_unitaire:.2f} €")
    
    def show_create_form(self):
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
                    self.get_available_statuses(),
                    format_func=self.get_status_display_name
                )
            
            submitted = st.form_submit_button("✅ Créer la commande")
            
            if submitted:
                if not adresse_livraison.strip():
                    self.show_error("L'adresse de livraison est obligatoire")
                else:
                    order_request = CreateOrderRequest(
                        utilisateur_id=utilisateur_id,
                        adresse_livraison=adresse_livraison,
                        statut=statut
                    )
                    
                    new_order = self.create_order(order_request)
                    if new_order:
                        st.rerun()
    
    def show_update_form(self, order_id: int):
        """Affiche le formulaire de mise à jour de commande"""
        order = self.get_order_by_id(order_id)
        if not order:
            self.show_error(f"Commande {order_id} non trouvée")
            return
        
        st.subheader(f"✏️ Modifier la Commande #{order_id}")
        
        with st.form("edit_order_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**ID:** {order.id}")
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
                    self.get_available_statuses(),
                    index=self.get_available_statuses().index(order.statut) if order.statut in self.get_available_statuses() else 0,
                    format_func=self.get_status_display_name
                )
            
            submitted = st.form_submit_button("✅ Mettre à jour la commande")
            
            if submitted:
                if not new_adresse_livraison.strip():
                    self.show_error("L'adresse de livraison est obligatoire")
                else:
                    update_request = UpdateOrderRequest(
                        utilisateur_id=new_utilisateur_id,
                        adresse_livraison=new_adresse_livraison,
                        statut=new_statut
                    )
                    
                    updated_order = self.update_order(order_id, update_request)
                    if updated_order:
                        st.rerun()
