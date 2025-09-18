"""
Présentateur pour la gestion des utilisateurs
"""

from typing import List, Optional
import streamlit as st
import pandas as pd
from presenters.base_presenter import BasePresenter
from models import User, CreateUserRequest, UpdateUserRequest


class UserPresenter(BasePresenter):
    """Présentateur pour la gestion des utilisateurs"""
    
    def __init__(self, user_service):
        super().__init__(user_service)
        self.user_service = user_service
    
    def show_list(self):
        """Affiche la liste des utilisateurs"""
        st.subheader("👥 Liste des Utilisateurs")
        
        with self.show_loading("Chargement des utilisateurs..."):
            users = self.service.get_all()
        
        if not users:
            st.info("Aucun utilisateur trouvé")
            return
        
        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            role_filter = st.selectbox(
                "Filtrer par rôle",
                ["Tous", "client", "admin"],
                key="user_role_filter"
            )
        
        with col2:
            search_term = st.text_input("Rechercher par nom ou email", key="user_search")
        
        # Appliquer les filtres
        filtered_users = users
        if role_filter != "Tous":
            filtered_users = [u for u in filtered_users if u.role == role_filter]
        
        if search_term:
            filtered_users = [
                u for u in filtered_users 
                if search_term.lower() in u.nom.lower() or search_term.lower() in u.email.lower()
            ]
        
        # Affichage des utilisateurs
        if filtered_users:
            # Créer un DataFrame
            df_data = []
            for user in filtered_users:
                df_data.append({
                    "ID": user.id,
                    "Nom": user.nom,
                    "Email": user.email,
                    "Rôle": user.role,
                    "Date création": user.date_creation.strftime("%d/%m/%Y") if user.date_creation else "N/A"
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Statistiques
            self.show_user_statistics(users)
        else:
            st.info("Aucun utilisateur ne correspond aux critères de recherche")
    
    def show_detail(self, user_id: int):
        """Affiche le détail d'un utilisateur"""
        st.subheader(f"👤 Détail de l'Utilisateur {user_id}")
        
        with self.show_loading("Chargement des détails..."):
            user = self.service.get_by_id(user_id)
        
        if not user:
            st.error("Utilisateur non trouvé")
            return
        
        # Affichage des informations
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Nom:** {user.nom}")
            st.write(f"**Email:** {user.email}")
        
        with col2:
            st.write(f"**Rôle:** {user.role}")
            st.write(f"**Date création:** {user.date_creation.strftime('%d/%m/%Y %H:%M') if user.date_creation else 'N/A'}")
        
        # Actions
        st.subheader("Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✏️ Modifier", key=f"edit_user_{user_id}"):
                st.session_state[f"edit_user_{user_id}"] = True
        
        with col2:
            if st.button("🗑️ Supprimer", key=f"delete_user_{user_id}"):
                st.session_state[f"confirm_delete_user_{user_id}"] = True
        
        with col3:
            if st.button("📋 Commandes", key=f"orders_user_{user_id}"):
                st.session_state["show_user_orders"] = user_id
        
        # Confirmation de suppression
        if st.session_state.get(f"confirm_delete_user_{user_id}"):
            st.warning("⚠️ Êtes-vous sûr de vouloir supprimer cet utilisateur ?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Confirmer", key=f"confirm_delete_yes_{user_id}"):
                    if self.service.delete(user_id):
                        st.rerun()
            with col2:
                if st.button("❌ Annuler", key=f"confirm_delete_no_{user_id}"):
                    st.session_state[f"confirm_delete_user_{user_id}"] = False
                    st.rerun()
    
    def show_create_form(self):
        """Affiche le formulaire de création d'utilisateur"""
        st.subheader("➕ Créer un Nouvel Utilisateur")
        
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                email = st.text_input("Email *", placeholder="exemple@email.com")
                nom = st.text_input("Nom *", placeholder="Nom complet")
            
            with col2:
                mot_de_passe = st.text_input("Mot de passe *", type="password")
                role = st.selectbox("Rôle", ["client", "admin"])
            
            submitted = st.form_submit_button("Créer l'utilisateur", type="primary")
            
            if submitted:
                if not all([email, nom, mot_de_passe]):
                    st.error("Veuillez remplir tous les champs obligatoires")
                else:
                    try:
                        user_request = CreateUserRequest(
                            email=email,
                            mot_de_passe=mot_de_passe,
                            nom=nom,
                            role=role
                        )
                        user = self.service.create(user_request)
                        if user:
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erreur lors de la création: {str(e)}")
    
    def show_update_form(self, user_id: int):
        """Affiche le formulaire de mise à jour d'utilisateur"""
        st.subheader(f"✏️ Modifier l'Utilisateur {user_id}")
        
        # Récupérer les données actuelles
        user = self.service.get_by_id(user_id)
        if not user:
            st.error("Utilisateur non trouvé")
            return
        
        with st.form("update_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                email = st.text_input("Email", value=user.email)
                nom = st.text_input("Nom", value=user.nom)
            
            with col2:
                role = st.selectbox("Rôle", ["client", "admin"], index=0 if user.role == "client" else 1)
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Mettre à jour", type="primary")
            with col2:
                if st.form_submit_button("Annuler"):
                    st.session_state[f"edit_user_{user_id}"] = False
                    st.rerun()
            
            if submitted:
                try:
                    user_request = UpdateUserRequest(
                        email=email,
                        nom=nom,
                        role=role
                    )
                    updated_user = self.service.update(user_id, user_request)
                    if updated_user:
                        st.session_state[f"edit_user_{user_id}"] = False
                        st.rerun()
                except Exception as e:
                    st.error(f"Erreur lors de la mise à jour: {str(e)}")
    
    def show_user_statistics(self, users: List[User]):
        """Affiche les statistiques des utilisateurs"""
        st.subheader("📊 Statistiques des Utilisateurs")
        
        stats = self.service.get_statistics()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Utilisateurs", stats["total"])
        with col2:
            st.metric("Clients", stats["clients"])
        with col3:
            st.metric("Administrateurs", stats["admins"])
        
        # Graphique des rôles
        if stats["total"] > 0:
            import plotly.express as px
            
            role_data = {
                "Rôle": ["Clients", "Administrateurs"],
                "Nombre": [stats["clients"], stats["admins"]]
            }
            
            fig = px.pie(
                values=role_data["Nombre"],
                names=role_data["Rôle"],
                title="Répartition par rôle"
            )
            st.plotly_chart(fig, use_container_width=True)
