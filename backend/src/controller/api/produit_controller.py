"""
Contrôleur API pour les produits
"""

from flask_restx import Namespace, Resource, fields
from ...service.impl import ProduitService
from ...controller.dto import ProduitDTO, CreateProduitDTO, UpdateProduitDTO
from ...utils.auth_decorators import token_required, admin_required

# Namespace pour les produits
produit_ns = Namespace('produits', description='Opérations sur les produits')

# Modèles Swagger
produit_model = produit_ns.model('Produit', {
    'id': fields.Integer(readonly=True, description='ID unique du produit'),
    'nom': fields.String(required=True, description='Nom du produit'),
    'description': fields.String(description='Description du produit'),
    'categorie': fields.String(required=True, description='Catégorie du produit'),
    'prix': fields.Float(required=True, description='Prix du produit'),
    'quantite_stock': fields.Integer(description='Quantité en stock'),
    'image_url': fields.String(description='URL de l\'image principale'),
    'images': fields.List(fields.String, description='Liste des URLs d\'images'),
    'date_creation': fields.DateTime(readonly=True, description='Date d\'ajout du produit')
})

produit_input_model = produit_ns.model('ProduitInput', {
    'nom': fields.String(required=True, description='Nom du produit'),
    'description': fields.String(description='Description du produit'),
    'categorie': fields.String(required=True, description='Catégorie du produit'),
    'prix': fields.Float(required=True, description='Prix du produit'),
    'quantite_stock': fields.Integer(description='Quantité en stock', default=0),
    'image_url': fields.String(description='URL de l\'image principale'),
    'images': fields.List(fields.String, description='Liste des URLs d\'images')
})

# Service
produit_service = ProduitService()


@produit_ns.route('/')
class ProduitList(Resource):
    @produit_ns.doc('list_produits')
    @produit_ns.marshal_list_with(produit_model)
    def get(self):
        """Récupère la liste de tous les produits"""
        products = produit_service.get_all_products()
        return [product.to_dict() for product in products]

    @produit_ns.doc('create_produit')
    @produit_ns.expect(produit_input_model)
    @produit_ns.marshal_with(produit_model, code=201)
    @admin_required
    def post(self):
        """Crée un nouveau produit (Admin uniquement)"""
        data = produit_ns.payload
        product = produit_service.create_product(
            nom=data['nom'],
            description=data.get('description'),
            categorie=data['categorie'],
            prix=data['prix'],
            quantite_stock=data.get('quantite_stock', 0)
        )
        return product.to_dict(), 201


@produit_ns.route('/<int:product_id>')
@produit_ns.param('product_id', 'ID du produit')
class Produit(Resource):
    @produit_ns.doc('get_produit')
    @produit_ns.marshal_with(produit_model)
    def get(self, product_id):
        """Récupère un produit par son ID"""
        product = produit_service.get_product_by_id(product_id)
        if not product:
            produit_ns.abort(404, f"Produit {product_id} non trouvé")
        return product.to_dict()

    @produit_ns.doc('update_produit')
    @produit_ns.expect(produit_input_model)
    @produit_ns.marshal_with(produit_model)
    @admin_required
    def put(self, product_id):
        """Met à jour un produit (Admin uniquement)"""
        data = produit_ns.payload
        # Supprimer l'id du payload pour éviter le conflit avec product_id
        if 'id' in data:
            del data['id']
        product = produit_service.update_product(product_id, **data)
        if not product:
            produit_ns.abort(404, f"Produit {product_id} non trouvé")
        return product.to_dict()

    @produit_ns.doc('delete_produit')
    @admin_required
    def delete(self, product_id):
        """Supprime un produit (Admin uniquement)"""
        success = produit_service.delete_product(product_id)
        if not success:
            produit_ns.abort(404, f"Produit {product_id} non trouvé")
        return '', 204


@produit_ns.route('/categorie/<string:categorie>')
@produit_ns.param('categorie', 'Catégorie du produit')
class ProduitsByCategorie(Resource):
    @produit_ns.doc('list_produits_by_categorie')
    @produit_ns.marshal_list_with(produit_model)
    def get(self, categorie):
        """Récupère tous les produits d'une catégorie"""
        products = produit_service.get_products_by_category(categorie)
        return [product.to_dict() for product in products]


@produit_ns.route('/prix/<float:min_price>/<float:max_price>')
@produit_ns.param('min_price', 'Prix minimum')
@produit_ns.param('max_price', 'Prix maximum')
class ProduitsByPriceRange(Resource):
    @produit_ns.doc('list_produits_by_price_range')
    @produit_ns.marshal_list_with(produit_model)
    def get(self, min_price, max_price):
        """Récupère les produits dans une fourchette de prix"""
        products = produit_service.get_products_by_price_range(min_price, max_price)
        return [product.to_dict() for product in products]


@produit_ns.route('/stock')
class ProduitsInStock(Resource):
    @produit_ns.doc('list_produits_in_stock')
    @produit_ns.marshal_list_with(produit_model)
    def get(self):
        """Récupère tous les produits en stock"""
        products = produit_service.get_products_in_stock()
        return [product.to_dict() for product in products]


@produit_ns.route('/<int:product_id>/stock')
@produit_ns.param('product_id', 'ID du produit')
class UpdateStock(Resource):
    @produit_ns.doc('update_stock')
    @produit_ns.expect(produit_ns.model('StockUpdate', {
        'quantite': fields.Integer(required=True, description='Nouvelle quantité en stock')
    }))
    @admin_required
    def put(self, product_id):
        """Met à jour le stock d'un produit (Admin uniquement)"""
        data = produit_ns.payload
        success = produit_service.update_stock(product_id, data['quantite'])
        if not success:
            produit_ns.abort(404, f"Produit {product_id} non trouvé")
        return {'message': f'Stock du produit {product_id} mis à jour'}, 200

