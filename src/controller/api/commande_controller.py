"""
Contrôleur API pour les commandes
"""

from flask_restx import Namespace, Resource, fields
from ...service.impl import CommandeService
from ...controller.dto import CommandeDTO, CreateCommandeDTO, UpdateCommandeDTO
from ...utils.auth_decorators import token_required, admin_required, client_or_admin_required

# Namespace pour les commandes
commande_ns = Namespace('commandes', description='Opérations sur les commandes')

# Modèles Swagger
ligne_commande_model = commande_ns.model('LigneCommande', {
    'id': fields.Integer(readonly=True, description='ID unique de la ligne'),
    'commande_id': fields.Integer(required=True, description='ID de la commande'),
    'produit_id': fields.Integer(required=True, description='ID du produit'),
    'quantite': fields.Integer(required=True, description='Quantité commandée'),
    'prix_unitaire': fields.Float(required=True, description='Prix unitaire'),
    'total_ligne': fields.Float(readonly=True, description='Total de la ligne')
})

commande_model = commande_ns.model('Commande', {
    'id': fields.Integer(readonly=True, description='ID unique de la commande'),
    'utilisateur_id': fields.Integer(required=True, description='ID de l\'utilisateur'),
    'date_commande': fields.DateTime(readonly=True, description='Date de la commande'),
    'adresse_livraison': fields.String(required=True, description='Adresse de livraison'),
    'statut': fields.String(description='Statut de la commande'),
    'lignes_commande': fields.List(fields.Nested(ligne_commande_model)),
    'total': fields.Float(readonly=True, description='Total de la commande')
})

commande_input_model = commande_ns.model('CommandeInput', {
    'utilisateur_id': fields.Integer(required=True, description='ID de l\'utilisateur'),
    'adresse_livraison': fields.String(required=True, description='Adresse de livraison'),
    'statut': fields.String(description='Statut de la commande', default='en_attente')
})

# Service
commande_service = CommandeService()


@commande_ns.route('/')
class CommandeList(Resource):
    @commande_ns.doc('list_commandes')
    @commande_ns.marshal_list_with(commande_model)
    @admin_required
    def get(self):
        """Récupère la liste de toutes les commandes (Admin uniquement)"""
        orders = commande_service.get_all_orders()
        return [order.to_dict() for order in orders]

    @commande_ns.doc('create_commande')
    @commande_ns.expect(commande_input_model)
    @commande_ns.marshal_with(commande_model, code=201)
    @client_or_admin_required
    def post(self):
        """Crée une nouvelle commande (Client ou Admin)"""
        data = commande_ns.payload
        order = commande_service.create_order(
            utilisateur_id=data['utilisateur_id'],
            adresse_livraison=data['adresse_livraison'],
            lignes_commande=data.get('lignes_commande', [])
        )
        return order.to_dict(), 201


@commande_ns.route('/<int:order_id>')
@commande_ns.param('order_id', 'ID de la commande')
class Commande(Resource):
    @commande_ns.doc('get_commande')
    @commande_ns.marshal_with(commande_model)
    @client_or_admin_required
    def get(self, order_id):
        """Récupère une commande par son ID (Client ou Admin)"""
        order = commande_service.get_order_by_id(order_id)
        if not order:
            commande_ns.abort(404, f"Commande {order_id} non trouvée")
        return order.to_dict()

    @commande_ns.doc('update_commande')
    @commande_ns.expect(commande_input_model)
    @commande_ns.marshal_with(commande_model)
    @admin_required
    def put(self, order_id):
        """Met à jour une commande (Admin uniquement)"""
        data = commande_ns.payload
        order = commande_service.update_order(order_id, **data)
        if not order:
            commande_ns.abort(404, f"Commande {order_id} non trouvée")
        return order.to_dict()

    @commande_ns.doc('delete_commande')
    @admin_required
    def delete(self, order_id):
        """Supprime une commande (Admin uniquement)"""
        success = commande_service.delete_order(order_id)
        if not success:
            commande_ns.abort(404, f"Commande {order_id} non trouvée")
        return '', 204


@commande_ns.route('/utilisateur/<int:user_id>')
@commande_ns.param('user_id', 'ID de l\'utilisateur')
class CommandesByUser(Resource):
    @commande_ns.doc('list_commandes_by_user')
    @commande_ns.marshal_list_with(commande_model)
    @client_or_admin_required
    def get(self, user_id):
        """Récupère toutes les commandes d'un utilisateur (Client ou Admin)"""
        orders = commande_service.get_orders_by_user(user_id)
        return [order.to_dict() for order in orders]


@commande_ns.route('/statut/<string:status>')
@commande_ns.param('status', 'Statut de la commande')
class CommandesByStatus(Resource):
    @commande_ns.doc('list_commandes_by_status')
    @commande_ns.marshal_list_with(commande_model)
    @admin_required
    def get(self, status):
        """Récupère toutes les commandes d'un statut donné (Admin uniquement)"""
        orders = commande_service.get_orders_by_status(status)
        return [order.to_dict() for order in orders]


@commande_ns.route('/<int:order_id>/statut')
@commande_ns.param('order_id', 'ID de la commande')
class UpdateOrderStatus(Resource):
    @commande_ns.doc('update_order_status')
    @commande_ns.expect(commande_ns.model('StatusUpdate', {
        'statut': fields.String(required=True, description='Nouveau statut')
    }))
    @admin_required
    def put(self, order_id):
        """Met à jour le statut d'une commande (Admin uniquement)"""
        data = commande_ns.payload
        success = commande_service.update_order_status(order_id, data['statut'])
        if not success:
            commande_ns.abort(404, f"Commande {order_id} non trouvée")
        return {'message': f'Statut de la commande {order_id} mis à jour'}, 200


@commande_ns.route('/<int:order_id>/total')
@commande_ns.param('order_id', 'ID de la commande')
class OrderTotal(Resource):
    @commande_ns.doc('get_order_total')
    @client_or_admin_required
    def get(self, order_id):
        """Calcule le total d'une commande (Client ou Admin)"""
        total = commande_service.calculate_order_total(order_id)
        if total == 0.0:
            commande_ns.abort(404, f"Commande {order_id} non trouvée")
        return {'order_id': order_id, 'total': total}, 200
