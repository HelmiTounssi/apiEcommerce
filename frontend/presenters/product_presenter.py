"""
Présentateur pour la gestion des produits
"""

from typing import List, Optional
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from presenters.base_presenter import BasePresenter
from models import Product, CreateProductRequest, UpdateProductRequest


class ProductPresenter(BasePresenter):
    """Présentateur pour la gestion des produits"""
    
    def __init__(self, product_service):
        super().__init__(product_service)
        self.product_service = product_service
    
    def show_list(self):
        """Affiche la liste des produits"""
        st.subheader("📦 Liste des Produits")
        
        with self.show_loading("Chargement des produits..."):
            products = self.service.get_all()
        
        if not products:
            st.info("Aucun produit trouvé")
            return
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox(
                "Filtrer par catégorie",
                ["Toutes"] + list(set(p.categorie for p in products)),
                key="product_category_filter"
            )
        
        with col2:
            stock_filter = st.selectbox(
                "Filtrer par stock",
                ["Tous", "En stock", "Rupture de stock"],
                key="product_stock_filter"
            )
        
        with col3:
            search_term = st.text_input("Rechercher par nom", key="product_search")
        
        # Appliquer les filtres
        filtered_products = products
        if category_filter != "Toutes":
            filtered_products = [p for p in filtered_products if p.categorie == category_filter]
        
        if stock_filter == "En stock":
            filtered_products = [p for p in filtered_products if p.quantite_stock > 0]
        elif stock_filter == "Rupture de stock":
            filtered_products = [p for p in filtered_products if p.quantite_stock == 0]
        
        if search_term:
            filtered_products = [
                p for p in filtered_products 
                if search_term.lower() in p.nom.lower()
            ]
        
        # Affichage des produits
        if filtered_products:
            # Créer un DataFrame
            df_data = []
            for product in filtered_products:
                stock_status = "✅ En stock" if product.quantite_stock > 0 else "❌ Rupture"
                df_data.append({
                    "ID": product.id,
                    "Nom": product.nom,
                    "Catégorie": product.categorie,
                    "Prix": f"{product.prix:.2f}€",
                    "Stock": product.quantite_stock,
                    "Statut": stock_status,
                    "Date création": product.date_creation.strftime("%d/%m/%Y") if product.date_creation else "N/A"
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Statistiques
            self.show_product_statistics(products)
        else:
            st.info("Aucun produit ne correspond aux critères de recherche")
    
    def show_detail(self, product_id: int):
        """Affiche le détail d'un produit"""
        st.subheader(f"📦 Détail du Produit {product_id}")
        
        with self.show_loading("Chargement des détails..."):
            product = self.service.get_by_id(product_id)
        
        if not product:
            st.error("Produit non trouvé")
            return
        
        # Affichage des informations
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Nom:** {product.nom}")
            st.write(f"**Catégorie:** {product.categorie}")
            st.write(f"**Prix:** {product.prix:.2f}€")
        
        with col2:
            stock_status = "✅ En stock" if product.quantite_stock > 0 else "❌ Rupture de stock"
            st.write(f"**Stock:** {product.quantite_stock} unités")
            st.write(f"**Statut:** {stock_status}")
            st.write(f"**Date création:** {product.date_creation.strftime('%d/%m/%Y %H:%M') if product.date_creation else 'N/A'}")
        
        if product.description:
            st.write(f"**Description:** {product.description}")
        
        # Actions
        st.subheader("Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✏️ Modifier", key=f"edit_product_{product_id}"):
                st.session_state[f"edit_product_{product_id}"] = True
        
        with col2:
            if st.button("📦 Gérer le stock", key=f"manage_stock_{product_id}"):
                st.session_state[f"manage_stock_{product_id}"] = True
        
        with col3:
            if st.button("🗑️ Supprimer", key=f"delete_product_{product_id}"):
                st.session_state[f"confirm_delete_product_{product_id}"] = True
        
        # Confirmation de suppression
        if st.session_state.get(f"confirm_delete_product_{product_id}"):
            st.warning("⚠️ Êtes-vous sûr de vouloir supprimer ce produit ?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Confirmer", key=f"confirm_delete_yes_{product_id}"):
                    if self.service.delete(product_id):
                        st.rerun()
            with col2:
                if st.button("❌ Annuler", key=f"confirm_delete_no_{product_id}"):
                    st.session_state[f"confirm_delete_product_{product_id}"] = False
                    st.rerun()
    
    def show_create_form(self):
        """Affiche le formulaire de création de produit"""
        st.subheader("➕ Créer un Nouveau Produit")
        
        with st.form("create_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom *", placeholder="Nom du produit")
                categorie = st.text_input("Catégorie *", placeholder="Catégorie du produit")
                prix = st.number_input("Prix *", min_value=0.0, step=0.01, format="%.2f")
            
            with col2:
                quantite_stock = st.number_input("Quantité en stock", min_value=0, value=0)
                description = st.text_area("Description", placeholder="Description du produit")
            
            submitted = st.form_submit_button("Créer le produit", type="primary")
            
            if submitted:
                if not all([nom, categorie, prix is not None]):
                    st.error("Veuillez remplir tous les champs obligatoires")
                else:
                    try:
                        product_request = CreateProductRequest(
                            nom=nom,
                            description=description if description else None,
                            categorie=categorie,
                            prix=prix,
                            quantite_stock=quantite_stock
                        )
                        product = self.service.create(product_request)
                        if product:
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erreur lors de la création: {str(e)}")
    
    def show_update_form(self, product_id: int):
        """Affiche le formulaire de mise à jour de produit"""
        st.subheader(f"✏️ Modifier le Produit {product_id}")
        
        # Récupérer les données actuelles
        product = self.service.get_by_id(product_id)
        if not product:
            st.error("Produit non trouvé")
            return
        
        with st.form("update_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nom = st.text_input("Nom", value=product.nom)
                categorie = st.text_input("Catégorie", value=product.categorie)
                prix = st.number_input("Prix", min_value=0.0, step=0.01, format="%.2f", value=product.prix)
            
            with col2:
                quantite_stock = st.number_input("Quantité en stock", min_value=0, value=product.quantite_stock)
                description = st.text_area("Description", value=product.description or "")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Mettre à jour", type="primary")
            with col2:
                if st.form_submit_button("Annuler"):
                    st.session_state[f"edit_product_{product_id}"] = False
                    st.rerun()
            
            if submitted:
                try:
                    product_request = UpdateProductRequest(
                        nom=nom,
                        description=description if description else None,
                        categorie=categorie,
                        prix=prix,
                        quantite_stock=quantite_stock
                    )
                    updated_product = self.service.update(product_id, product_request)
                    if updated_product:
                        st.session_state[f"edit_product_{product_id}"] = False
                        st.rerun()
                except Exception as e:
                    st.error(f"Erreur lors de la mise à jour: {str(e)}")
    
    def show_stock_management(self, product_id: int):
        """Affiche la gestion du stock d'un produit"""
        st.subheader(f"📦 Gestion du Stock - Produit {product_id}")
        
        product = self.service.get_by_id(product_id)
        if not product:
            st.error("Produit non trouvé")
            return
        
        st.write(f"**Produit:** {product.nom}")
        st.write(f"**Stock actuel:** {product.quantite_stock} unités")
        
        with st.form("stock_management_form"):
            new_quantity = st.number_input(
                "Nouvelle quantité en stock",
                min_value=0,
                value=product.quantite_stock
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Mettre à jour le stock", type="primary")
            with col2:
                if st.form_submit_button("Annuler"):
                    st.session_state[f"manage_stock_{product_id}"] = False
                    st.rerun()
            
            if submitted:
                if self.service.update_stock(product_id, new_quantity):
                    st.session_state[f"manage_stock_{product_id}"] = False
                    st.rerun()
    
    def show_product_statistics(self, products: List[Product]):
        """Affiche les statistiques des produits"""
        st.subheader("📊 Statistiques des Produits")
        
        stats = self.service.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Produits", stats["total"])
        with col2:
            st.metric("En Stock", stats["in_stock"])
        with col3:
            st.metric("Rupture", stats["out_of_stock"])
        with col4:
            st.metric("Valeur Stock", f"{stats['total_value']:.2f}€")
        
        # Graphiques
        if stats["total"] > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition par catégorie
                if stats["categories"]:
                    fig = px.pie(
                        values=list(stats["categories"].values()),
                        names=list(stats["categories"].keys()),
                        title="Répartition par catégorie"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # État du stock
                stock_data = {
                    "État": ["En stock", "Rupture"],
                    "Nombre": [stats["in_stock"], stats["out_of_stock"]]
                }
                fig = px.bar(
                    x=stock_data["État"],
                    y=stock_data["Nombre"],
                    title="État du stock"
                )
                st.plotly_chart(fig, use_container_width=True)
