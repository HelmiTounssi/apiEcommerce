"""
Contrôleur API pour les utilisateurs
"""

from flask_restx import Namespace, Resource, fields
from ...service.impl import UtilisateurService
from ...controller.dto import UtilisateurDTO, CreateUtilisateurDTO, UpdateUtilisateurDTO

# Namespace pour les utilisateurs
utilisateur_ns = Namespace('utilisateurs', description='Opérations sur les utilisateurs')

# Modèles Swagger
utilisateur_model = utilisateur_ns.model('Utilisateur', {
    'id': fields.Integer(readonly=True, description='ID unique de l\'utilisateur'),
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'nom': fields.String(required=True, description='Nom de l\'utilisateur'),
    'role': fields.String(description='Rôle de l\'utilisateur (client ou admin)'),
    'date_creation': fields.DateTime(readonly=True, description='Date de création du compte')
})

utilisateur_input_model = utilisateur_ns.model('UtilisateurInput', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'mot_de_passe': fields.String(required=True, description='Mot de passe'),
    'nom': fields.String(required=True, description='Nom de l\'utilisateur'),
    'role': fields.String(description='Rôle de l\'utilisateur (client ou admin)', default='client')
})

# Service
utilisateur_service = UtilisateurService()


@utilisateur_ns.route('/')
class UtilisateurList(Resource):
    @utilisateur_ns.doc('list_utilisateurs')
    @utilisateur_ns.marshal_list_with(utilisateur_model)
    def get(self):
        """Récupère la liste de tous les utilisateurs"""
        users = utilisateur_service.get_all_users()
        return [user.to_dict() for user in users]

    @utilisateur_ns.doc('create_utilisateur')
    @utilisateur_ns.expect(utilisateur_input_model)
    @utilisateur_ns.marshal_with(utilisateur_model, code=201)
    def post(self):
        """Crée un nouvel utilisateur"""
        data = utilisateur_ns.payload
        user = utilisateur_service.create_user(
            email=data['email'],
            password=data['mot_de_passe'],
            nom=data['nom'],
            role=data.get('role', 'client')
        )
        return user.to_dict(), 201


@utilisateur_ns.route('/<int:user_id>')
@utilisateur_ns.param('user_id', 'ID de l\'utilisateur')
class Utilisateur(Resource):
    @utilisateur_ns.doc('get_utilisateur')
    @utilisateur_ns.marshal_with(utilisateur_model)
    def get(self, user_id):
        """Récupère un utilisateur par son ID"""
        user = utilisateur_service.get_user_by_id(user_id)
        if not user:
            utilisateur_ns.abort(404, f"Utilisateur {user_id} non trouvé")
        return user.to_dict()

    @utilisateur_ns.doc('update_utilisateur')
    @utilisateur_ns.expect(utilisateur_input_model)
    @utilisateur_ns.marshal_with(utilisateur_model)
    def put(self, user_id):
        """Met à jour un utilisateur"""
        data = utilisateur_ns.payload
        user = utilisateur_service.update_user(user_id, **data)
        if not user:
            utilisateur_ns.abort(404, f"Utilisateur {user_id} non trouvé")
        return user.to_dict()

    @utilisateur_ns.doc('delete_utilisateur')
    def delete(self, user_id):
        """Supprime un utilisateur"""
        success = utilisateur_service.delete_user(user_id)
        if not success:
            utilisateur_ns.abort(404, f"Utilisateur {user_id} non trouvé")
        return '', 204


@utilisateur_ns.route('/email/<string:email>')
@utilisateur_ns.param('email', 'Email de l\'utilisateur')
class UtilisateurByEmail(Resource):
    @utilisateur_ns.doc('get_utilisateur_by_email')
    @utilisateur_ns.marshal_with(utilisateur_model)
    def get(self, email):
        """Récupère un utilisateur par son email"""
        user = utilisateur_service.get_user_by_email(email)
        if not user:
            utilisateur_ns.abort(404, f"Utilisateur avec email {email} non trouvé")
        return user.to_dict()


@utilisateur_ns.route('/role/<string:role>')
@utilisateur_ns.param('role', 'Rôle de l\'utilisateur')
class UtilisateursByRole(Resource):
    @utilisateur_ns.doc('list_utilisateurs_by_role')
    @utilisateur_ns.marshal_list_with(utilisateur_model)
    def get(self, role):
        """Récupère tous les utilisateurs d'un rôle donné"""
        users = utilisateur_service.get_users_by_role(role)
        return [user.to_dict() for user in users]

