"""
Vue pour la configuration et les statistiques
"""

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any

class ConfigStatsView:
    """Vue pour la configuration et les statistiques"""
    
    def __init__(self, api_base_url: str = "http://localhost:5000"):
        self.api_base_url = api_base_url
    
    def show_config_stats_page(self, auth_token: str = None):
        """Affiche la page de configuration et statistiques"""
        st.title("⚙️ Configuration & Statistiques")
        
        # Onglets
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistiques", "⚙️ Configuration", "🔧 Maintenance", "📈 Rapports"])
        
        with tab1:
            self.show_statistics_tab(auth_token)
        
        with tab2:
            self.show_configuration_tab(auth_token)
        
        with tab3:
            self.show_maintenance_tab(auth_token)
        
        with tab4:
            self.show_reports_tab(auth_token)
    
    def show_statistics_tab(self, auth_token: str = None):
        """Affiche l'onglet des statistiques"""
        st.header("📊 Statistiques du Système")
        
        # Récupérer les statistiques
        stats = self.get_system_statistics(auth_token)
        
        if stats:
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="👥 Utilisateurs",
                    value=stats.get('users', {}).get('total', 0),
                    delta=stats.get('users', {}).get('new_today', 0)
                )
            
            with col2:
                st.metric(
                    label="📦 Produits",
                    value=stats.get('products', {}).get('total', 0),
                    delta=stats.get('products', {}).get('new_today', 0)
                )
            
            with col3:
                st.metric(
                    label="🛒 Commandes",
                    value=stats.get('orders', {}).get('total', 0),
                    delta=stats.get('orders', {}).get('new_today', 0)
                )
            
            with col4:
                st.metric(
                    label="💰 CA Total",
                    value=f"{stats.get('revenue', {}).get('total', 0):.2f} €",
                    delta=f"{stats.get('revenue', {}).get('today', 0):.2f} €"
                )
            
            # Graphiques
            col1, col2 = st.columns(2)
            
            with col1:
                self.show_orders_chart(stats.get('orders_chart', []))
            
            with col2:
                self.show_revenue_chart(stats.get('revenue_chart', []))
            
            # Statistiques détaillées
            st.subheader("📈 Statistiques Détaillées")
            
            # Tableau des commandes par statut
            orders_by_status = stats.get('orders_by_status', [])
            if orders_by_status:
                df_status = pd.DataFrame(orders_by_status)
                st.dataframe(df_status, use_container_width=True)
            
            # Top produits
            top_products = stats.get('top_products', [])
            if top_products:
                st.subheader("🏆 Top Produits")
                df_products = pd.DataFrame(top_products)
                st.dataframe(df_products, use_container_width=True)
        else:
            st.error("❌ Impossible de récupérer les statistiques")
    
    def show_configuration_tab(self, auth_token: str = None):
        """Affiche l'onglet de configuration"""
        st.header("⚙️ Configuration du Système")
        
        # Configuration de l'application
        st.subheader("🔧 Paramètres de l'Application")
        
        with st.form("config_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Paramètres Généraux**")
                app_name = st.text_input("Nom de l'application", value="E-commerce API")
                debug_mode = st.checkbox("Mode Debug", value=False)
                maintenance_mode = st.checkbox("Mode Maintenance", value=False)
                
                st.write("**Base de Données**")
                db_type = st.selectbox("Type de base de données", ["SQLite", "PostgreSQL", "MySQL"])
                db_pool_size = st.number_input("Taille du pool de connexions", min_value=1, max_value=100, value=10)
            
            with col2:
                st.write("**API**")
                api_timeout = st.number_input("Timeout API (secondes)", min_value=1, max_value=300, value=30)
                max_requests_per_minute = st.number_input("Max requêtes/minute", min_value=1, max_value=1000, value=100)
                
                st.write("**Sécurité**")
                jwt_expiration = st.number_input("Expiration JWT (heures)", min_value=1, max_value=24, value=1)
                password_min_length = st.number_input("Longueur min mot de passe", min_value=6, max_value=20, value=8)
            
            if st.form_submit_button("💾 Sauvegarder la Configuration"):
                config_data = {
                    "app_name": app_name,
                    "debug_mode": debug_mode,
                    "maintenance_mode": maintenance_mode,
                    "database": {
                        "type": db_type,
                        "pool_size": db_pool_size
                    },
                    "api": {
                        "timeout": api_timeout,
                        "max_requests_per_minute": max_requests_per_minute
                    },
                    "security": {
                        "jwt_expiration": jwt_expiration,
                        "password_min_length": password_min_length
                    }
                }
                
                if self.save_configuration(config_data, auth_token):
                    st.success("✅ Configuration sauvegardée avec succès !")
                else:
                    st.error("❌ Erreur lors de la sauvegarde de la configuration")
        
        # Configuration actuelle
        st.subheader("📋 Configuration Actuelle")
        current_config = self.get_current_configuration(auth_token)
        
        if current_config:
            st.json(current_config)
        else:
            st.warning("⚠️ Impossible de récupérer la configuration actuelle")
    
    def show_maintenance_tab(self, auth_token: str = None):
        """Affiche l'onglet de maintenance"""
        st.header("🔧 Maintenance du Système")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🗄️ Base de Données")
            
            if st.button("🔄 Optimiser la Base de Données"):
                if self.optimize_database(auth_token):
                    st.success("✅ Base de données optimisée !")
                else:
                    st.error("❌ Erreur lors de l'optimisation")
            
            if st.button("🧹 Nettoyer les Données Temporaires"):
                if self.cleanup_temp_data(auth_token):
                    st.success("✅ Données temporaires nettoyées !")
                else:
                    st.error("❌ Erreur lors du nettoyage")
            
            if st.button("📊 Analyser les Performances"):
                perf_data = self.analyze_performance(auth_token)
                if perf_data:
                    st.success("✅ Analyse terminée !")
                    st.json(perf_data)
                else:
                    st.error("❌ Erreur lors de l'analyse")
        
        with col2:
            st.subheader("🔄 Redémarrage")
            
            if st.button("🔄 Redémarrer l'API"):
                if self.restart_api(auth_token):
                    st.success("✅ API redémarrée !")
                else:
                    st.error("❌ Erreur lors du redémarrage")
            
            if st.button("🔄 Redémarrer le Cache"):
                if self.restart_cache(auth_token):
                    st.success("✅ Cache redémarré !")
                else:
                    st.error("❌ Erreur lors du redémarrage du cache")
        
        # Logs système
        st.subheader("📝 Logs Système")
        
        log_level = st.selectbox("Niveau de log", ["DEBUG", "INFO", "WARNING", "ERROR"])
        log_lines = st.number_input("Nombre de lignes", min_value=10, max_value=1000, value=100)
        
        if st.button("📋 Afficher les Logs"):
            logs = self.get_system_logs(log_level, log_lines, auth_token)
            if logs:
                st.text_area("Logs", logs, height=400)
            else:
                st.error("❌ Impossible de récupérer les logs")
    
    def show_reports_tab(self, auth_token: str = None):
        """Affiche l'onglet des rapports"""
        st.header("📈 Rapports")
        
        # Sélection de la période
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Date de début", value=datetime.now() - timedelta(days=30))
        
        with col2:
            end_date = st.date_input("Date de fin", value=datetime.now())
        
        # Types de rapports
        report_type = st.selectbox("Type de rapport", [
            "Ventes par période",
            "Top clients",
            "Produits les plus vendus",
            "Analyse des commandes",
            "Performance du système"
        ])
        
        if st.button("📊 Générer le Rapport"):
            report_data = self.generate_report(report_type, start_date, end_date, auth_token)
            
            if report_data:
                st.success("✅ Rapport généré avec succès !")
                
                # Afficher le rapport
                if report_type == "Ventes par période":
                    self.show_sales_report(report_data)
                elif report_type == "Top clients":
                    self.show_top_clients_report(report_data)
                elif report_type == "Produits les plus vendus":
                    self.show_top_products_report(report_data)
                elif report_type == "Analyse des commandes":
                    self.show_orders_analysis_report(report_data)
                elif report_type == "Performance du système":
                    self.show_performance_report(report_data)
            else:
                st.error("❌ Erreur lors de la génération du rapport")
    
    def show_orders_chart(self, data: List[Dict]):
        """Affiche le graphique des commandes"""
        if not data:
            st.info("Aucune donnée disponible")
            return
        
        df = pd.DataFrame(data)
        fig = px.line(df, x='date', y='count', title='Commandes par Jour')
        st.plotly_chart(fig, use_container_width=True)
    
    def show_revenue_chart(self, data: List[Dict]):
        """Affiche le graphique du chiffre d'affaires"""
        if not data:
            st.info("Aucune donnée disponible")
            return
        
        df = pd.DataFrame(data)
        fig = px.bar(df, x='date', y='revenue', title='Chiffre d\'Affaires par Jour')
        st.plotly_chart(fig, use_container_width=True)
    
    def show_sales_report(self, data: Dict):
        """Affiche le rapport des ventes"""
        st.subheader("📊 Rapport des Ventes")
        
        # Métriques principales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Ventes", f"{data.get('total_sales', 0):.2f} €")
        
        with col2:
            st.metric("Nombre de Commandes", data.get('total_orders', 0))
        
        with col3:
            st.metric("Panier Moyen", f"{data.get('average_order', 0):.2f} €")
        
        # Graphique des ventes
        if 'sales_data' in data:
            df = pd.DataFrame(data['sales_data'])
            fig = px.line(df, x='date', y='sales', title='Évolution des Ventes')
            st.plotly_chart(fig, use_container_width=True)
    
    def show_top_clients_report(self, data: Dict):
        """Affiche le rapport des top clients"""
        st.subheader("👥 Top Clients")
        
        if 'clients' in data:
            df = pd.DataFrame(data['clients'])
            st.dataframe(df, use_container_width=True)
    
    def show_top_products_report(self, data: Dict):
        """Affiche le rapport des produits les plus vendus"""
        st.subheader("🏆 Produits les Plus Vendus")
        
        if 'products' in data:
            df = pd.DataFrame(data['products'])
            st.dataframe(df, use_container_width=True)
    
    def show_orders_analysis_report(self, data: Dict):
        """Affiche l'analyse des commandes"""
        st.subheader("🛒 Analyse des Commandes")
        
        # Statistiques par statut
        if 'status_analysis' in data:
            st.write("**Répartition par Statut**")
            df_status = pd.DataFrame(data['status_analysis'])
            st.dataframe(df_status, use_container_width=True)
        
        # Évolution temporelle
        if 'temporal_analysis' in data:
            st.write("**Évolution Temporelle**")
            df_temp = pd.DataFrame(data['temporal_analysis'])
            fig = px.line(df_temp, x='date', y='count', title='Évolution des Commandes')
            st.plotly_chart(fig, use_container_width=True)
    
    def show_performance_report(self, data: Dict):
        """Affiche le rapport de performance"""
        st.subheader("⚡ Performance du Système")
        
        # Métriques de performance
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Temps de Réponse Moyen", f"{data.get('avg_response_time', 0):.2f} ms")
        
        with col2:
            st.metric("Requêtes/Minute", data.get('requests_per_minute', 0))
        
        with col3:
            st.metric("Taux d'Erreur", f"{data.get('error_rate', 0):.2f}%")
        
        # Graphique de performance
        if 'performance_data' in data:
            df = pd.DataFrame(data['performance_data'])
            fig = px.line(df, x='time', y='response_time', title='Temps de Réponse')
            st.plotly_chart(fig, use_container_width=True)
    
    # Méthodes API
    def get_system_statistics(self, auth_token: str = None) -> Dict:
        """Récupère les statistiques du système"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            response = requests.get(f"{self.api_base_url}/api/stats/", headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Erreur API: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Erreur de connexion: {e}")
            return None
    
    def get_current_configuration(self, auth_token: str = None) -> Dict:
        """Récupère la configuration actuelle"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            response = requests.get(f"{self.api_base_url}/api/config/", headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None
    
    def save_configuration(self, config_data: Dict, auth_token: str = None) -> bool:
        """Sauvegarde la configuration"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            response = requests.post(f"{self.api_base_url}/api/config/", 
                                   json=config_data, headers=headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def optimize_database(self, auth_token: str = None) -> bool:
        """Optimise la base de données"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            response = requests.post(f"{self.api_base_url}/api/maintenance/optimize-db", 
                                   headers=headers, timeout=30)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def cleanup_temp_data(self, auth_token: str = None) -> bool:
        """Nettoie les données temporaires"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            response = requests.post(f"{self.api_base_url}/api/maintenance/cleanup", 
                                   headers=headers, timeout=30)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def analyze_performance(self, auth_token: str = None) -> Dict:
        """Analyse les performances"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            response = requests.get(f"{self.api_base_url}/api/maintenance/performance", 
                                  headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None
    
    def restart_api(self, auth_token: str = None) -> bool:
        """Redémarre l'API"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            response = requests.post(f"{self.api_base_url}/api/maintenance/restart", 
                                   headers=headers, timeout=30)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def restart_cache(self, auth_token: str = None) -> bool:
        """Redémarre le cache"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            response = requests.post(f"{self.api_base_url}/api/maintenance/restart-cache", 
                                   headers=headers, timeout=30)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def get_system_logs(self, level: str, lines: int, auth_token: str = None) -> str:
        """Récupère les logs système"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            params = {"level": level, "lines": lines}
            response = requests.get(f"{self.api_base_url}/api/maintenance/logs", 
                                  params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            return None
    
    def generate_report(self, report_type: str, start_date, end_date, auth_token: str = None) -> Dict:
        """Génère un rapport"""
        try:
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            params = {
                "type": report_type,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
            response = requests.get(f"{self.api_base_url}/api/reports/generate", 
                                  params=params, headers=headers, timeout=60)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None
