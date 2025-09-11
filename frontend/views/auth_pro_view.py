"""
Vues d'authentification professionnelles
Interface moderne avec onglets et design cohérent
"""

import streamlit as st
from ..services.auth_service import get_auth_service


def show_auth():
    """Affiche l'interface d'authentification avec onglets"""

    # Conteneur principal avec style
    with st.container():
        # Onglets pour connexion/inscription
        tab1, tab2 = st.tabs(["🔐 Connexion", "📝 Inscription"])

        with tab1:
            show_login_form()

        with tab2:
            show_register_form()

        # Section des comptes de test
        show_test_accounts()

        # Section d'aide contextuelle
        show_help_section()


def show_login_form():
    """Affiche le formulaire de connexion"""

    st.markdown("""
    <div style="
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    ">
    """, unsafe_allow_html=True)

    auth_service = get_auth_service()

    with st.form("login_form", clear_on_submit=False):
        st.markdown("### 🔐 Connexion à votre compte")
        st.markdown(
    "Entrez vos identifiants pour accéder à votre espace personnel.")

        col1, col2 = st.columns([1, 1])

        with col1:
            email = st.text_input(
                "📧 Adresse email",
                placeholder="votre@email.com",
                help="Entrez votre adresse email de connexion"
            )

        with col2:
            password = st.text_input(
                "🔒 Mot de passe",
                type="password",
                placeholder="Votre mot de passe",
                help="Entrez votre mot de passe"
            )

        # Boutons d'action
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            submit_login = st.form_submit_button(
                "🚀 Se connecter",
                use_container_width=True,
                type="primary"
            )

        if submit_login:
            if email and password:
                try:
                    result = auth_service.login(email, password)
                    if result and result.get('success'):
                        st.success("✅ Connexion réussie!")
                        st.balloons()
                        st.rerun()
                    else:
                        # Afficher le message d'erreur détaillé
                        error_message = (
                            result.get('message', 'Email ou mot de passe incorrect') if result else 'Email ou mot de passe incorrect'
                        )
                        error_type = (
                            result.get('error', 'authentication_error') if result else 'authentication_error'
                        )

                        # Affichage ergonomique selon le type d'erreur
                        if error_type == 'authentication_error':
                            st.error(
    f"❌ **Identifiants incorrects** : {error_message}")
                            st.info("💡 **Solutions possibles :**")
                            st.markdown("""
                            - Vérifiez votre adresse email
                            - Vérifiez votre mot de passe
                            - Assurez-vous que votre compte existe
                            - Utilisez les comptes de test si nécessaire
                            """)
                        elif error_type == 'connection_error':
                            st.error(
    f"❌ **Erreur de connexion** : {error_message}")
                            st.info(
    "💡 **Solution :** Vérifiez que le serveur backend est démarré.")
                        else:
                            st.error(
    f"❌ **Erreur de connexion** : {error_message}")
                            st.info(
    "💡 **Solution :** Vérifiez vos identifiants et réessayez.")

                except Exception as e:
                    st.error(f"❌ **Erreur technique** : {str(e)}")
                    st.info(
    "💡 **Solution :** Vérifiez votre connexion et réessayez.")
            else:
                st.warning("⚠️ **Champs manquants** : Veuillez remplir tous les champs.")
                st.info("💡 **Champs requis :** Email et Mot de passe")

    st.markdown("</div>", unsafe_allow_html=True)


def show_register_form():
    """Affiche le formulaire d'inscription"""

    st.markdown("""
    <div style="
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    ">
    """, unsafe_allow_html=True)

    auth_service = get_auth_service()

    with st.form("register_form", clear_on_submit=False):
        st.markdown("### 📝 Créer un nouveau compte")
        st.markdown(
    "Remplissez le formulaire ci-dessous pour créer votre compte.")

        # Informations personnelles
        col1, col2 = st.columns([1, 1])

        with col1:
            nom = st.text_input(
                "👤 Nom complet",
                placeholder="Jean Dupont",
                help="Entrez votre nom complet"
            )

            email = st.text_input(
                "📧 Adresse email",
                placeholder="jean.dupont@email.com",
                help="Cette adresse servira d'identifiant de connexion"
            )

        with col2:
            role = st.selectbox(
                "👥 Type de compte",
                ["client", "admin"],
                help="Sélectionnez le type de compte (admin nécessite validation)"
            )

            password = st.text_input(
                "🔒 Mot de passe",
                type="password",
                placeholder="Mot de passe sécurisé",
                help="Choisissez un mot de passe fort"
            )

        # Boutons d'action
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            submit_register = st.form_submit_button(
                "✨ Créer mon compte",
                use_container_width=True,
                type="primary"
            )

        if submit_register:
            if nom and email and password:
                try:
                    result = auth_service.register(email, password, nom, role)
                    if result and result.get('success'):
                        st.success("✅ Compte créé avec succès!")
                        st.info(
    "🎉 Vous pouvez maintenant vous connecter avec vos identifiants.")
                        st.balloons()
                    else:
                        # Afficher le message d'erreur détaillé
                        error_message = (
                            result.get('message', 'Erreur lors de la création du compte') if result else 'Erreur lors de la création du compte'
                        )
                        error_type = (
                            result.get('error', 'unknown_error') if result else 'unknown_error'
                        )

                        # Affichage ergonomique selon le type d'erreur
                        if error_type == 'validation_error':
                            st.error(
    f"❌ **Erreur de validation** : {error_message}")
                            st.info("💡 **Solutions possibles :**")
                            st.markdown("""
                            - Vérifiez que tous les champs sont remplis
                            - Assurez-vous que l'email a un format valide (ex: nom@email.com)
                            - Le mot de passe ne doit pas être vide
                            - Le nom ne doit pas être vide
                            """)
                        elif 'email' in error_message.lower() and 'existe' in error_message.lower():
                            st.error(
    f"❌ **Email déjà utilisé** : {error_message}")
                            st.info(
    "💡 **Solution :** Utilisez un email différent qui n'est pas encore utilisé.")
                            st.markdown("""
                            **Exemples d'emails uniques :**
                            - `votre_nom@example.com`
                            - `test123@example.com`
                            - `mon_compte@example.com`
                            """)
                        elif error_type == 'connection_error':
                            st.error(
    f"❌ **Erreur de connexion** : {error_message}")
                            st.info(
    "💡 **Solution :** Vérifiez que le serveur backend est démarré.")
                        else:
                            st.error(
    f"❌ **Erreur d'inscription** : {error_message}")
                            st.info(
    "💡 **Solution :** Vérifiez vos données et réessayez.")

                except Exception as e:
                    st.error(f"❌ **Erreur technique** : {str(e)}")
                    st.info(
    "💡 **Solution :** Vérifiez votre connexion et réessayez.")
            else:
                st.warning("⚠️ **Champs manquants** : Veuillez remplir tous les champs obligatoires.")
                st.info("💡 **Champs requis :** Nom, Email, Mot de passe")

    st.markdown("</div>", unsafe_allow_html=True)


def show_test_accounts():
    """Affiche les comptes de test disponibles"""

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #00d4aa;
        margin-top: 2rem;
    ">
    """, unsafe_allow_html=True)

    st.markdown("### 🧪 Comptes de test disponibles")
    st.markdown("Utilisez ces comptes pour tester l'application :")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **👑 Compte Administrateur**
        - Email: `admin@ecommerce.com`
        - Mot de passe: `admin123`
        - Accès: Toutes les fonctionnalités
        """)

    with col2:
        st.markdown("""
        **👤 Compte Client**
        - Email: `client1@example.com`
        - Mot de passe: `client123`
        - Accès: Catalogue et commandes
        """)

    # Boutons de connexion rapide
    st.markdown("**🚀 Connexion rapide :**")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔑 Se connecter en tant qu'admin", use_container_width=True):
            auth_service = get_auth_service()
            try:
                result = auth_service.login("admin@ecommerce.com", "admin123")
                if result:
                    st.success("✅ Connexion admin réussie!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

    with col2:
        if st.button("👤 Se connecter en tant que client", use_container_width=True):
            auth_service = get_auth_service()
            try:
                result = auth_service.login("client1@example.com", "client123")
                if result:
                    st.success("✅ Connexion client réussie!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)


def show_help_section():
    """Affiche la section d'aide contextuelle"""

    with st.expander("❓ Aide et résolution de problèmes", expanded=False):
        st.markdown("""
        ### 🔧 Problèmes courants et solutions

        **❌ Erreur 400 - Email déjà utilisé**
        - **Cause :** L'email que vous utilisez existe déjà dans la base de données
        - **Solution :** Utilisez un email différent et unique
        - **Exemples :** `votre_nom@example.com`, `test123@example.com`

        **❌ Erreur 401 - Identifiants incorrects**
        - **Cause :** Email ou mot de passe incorrect
        - **Solution :** Vérifiez vos identifiants ou utilisez les comptes de test

        **❌ Erreur de connexion**
        - **Cause :** Le serveur backend n'est pas accessible
        - **Solution :** Vérifiez que le backend est démarré (http://localhost:5000)

        **❌ Champs manquants**
        - **Cause :** Un ou plusieurs champs obligatoires sont vides
        - **Solution :** Remplissez tous les champs marqués comme obligatoires

        ### 📋 Conseils d'utilisation

        - **Pour l'inscription :** Utilisez un email unique et un mot de passe sécurisé
        - **Pour la connexion :** Vérifiez que votre compte existe avant de vous connecter
        - **En cas de problème :** Utilisez les comptes de test pour vérifier le fonctionnement
        - **Support :** Vérifiez les logs du backend pour plus de détails techniques
        """)


def show_user_profile():
    """Affiche le profil utilisateur avec options de gestion"""

    auth_service = get_auth_service()

    if not auth_service.is_authenticated():
        st.error("🔒 Vous devez être connecté pour accéder à cette page.")
        st.info("Utilisez le bouton de connexion dans la sidebar.")
        return

    user = auth_service.get_current_user()

    if not user:
        st.error("❌ Impossible de récupérer les informations utilisateur.")
        return

    # En-tête du profil
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <div style="
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            font-size: 2rem;
        ">
            {(user.get('nom') or 'U')[0].upper()}
        </div>
        <h2 style="margin: 0; font-size: 1.8rem;">{user.get('nom', 'Utilisateur')}</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">{user.get('email', '')}</p>
        <span style="
            background: {'#ff6b6b' if user.get('role') == 'admin' else '#00d4aa'};
            color: white;
            padding: 0.25rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        ">{(user.get('role') or 'client').title()}</span>
    </div>
    """, unsafe_allow_html=True)

    # Informations du profil
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        ">
        """, unsafe_allow_html=True)

        st.markdown("### 📋 Informations personnelles")

        st.markdown(f"**👤 Nom :** {user.get('nom', 'N/A')}")
        st.markdown(f"**📧 Email :** {user.get('email', 'N/A')}")
        st.markdown(f"**👥 Rôle :** {(user.get('role') or 'N/A').title()}")
        st.markdown(f"**🆔 ID :** {user.get('id', 'N/A')}")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        ">
        """, unsafe_allow_html=True)

        st.markdown("### ⚙️ Actions")

        if st.button("🔄 Actualiser le profil", use_container_width=True):
            st.rerun()

        if st.button("✏️ Modifier le profil", use_container_width=True):
            st.info(
    "🚧 Fonctionnalité de modification en cours de développement.")

        if st.button("🔒 Changer le mot de passe", use_container_width=True):
            st.info(
    "🚧 Fonctionnalité de changement de mot de passe en cours de développement.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Statistiques utilisateur (si client)
    if user.get('role') == 'client':
        st.markdown("### 📊 Mes statistiques")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🛒 Commandes", "0", "0")

        with col2:
            st.metric("💰 Total dépensé", "0€", "0€")

        with col3:
            st.metric("⭐ Évaluation", "5.0", "0.0")

