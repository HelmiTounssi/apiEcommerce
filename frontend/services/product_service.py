"""
Service pour la gestion des produits
"""

from typing import List, Optional
from services.base_service import BaseService
from models import Product, CreateProductRequest, UpdateProductRequest, UpdateStockRequest


class ProductService(BaseService):
    """Service pour la gestion des produits"""
    
    def get_all(self) -> List[Product]:
        """Récupère tous les produits"""
        try:
            products_data = self.api_client.get_products()
            return [Product.from_dict(product_data) for product_data in products_data]
        except Exception as e:
            self.handle_error(e, "récupération des produits")
            return []
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Récupère un produit par ID"""
        try:
            product_data = self.api_client.get_product(product_id)
            return Product.from_dict(product_data) if product_data else None
        except Exception as e:
            self.handle_error(e, f"récupération du produit {product_id}")
            return None
    
    def get_by_category(self, category: str) -> List[Product]:
        """Récupère les produits par catégorie"""
        try:
            products_data = self.api_client.get_products_by_category(category)
            return [Product.from_dict(product_data) for product_data in products_data]
        except Exception as e:
            self.handle_error(e, f"récupération des produits {category}")
            return []
    
    def get_in_stock(self) -> List[Product]:
        """Récupère les produits en stock"""
        try:
            products_data = self.api_client.get_products_in_stock()
            return [Product.from_dict(product_data) for product_data in products_data]
        except Exception as e:
            self.handle_error(e, "récupération des produits en stock")
            return []
    
    def get_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Récupère les produits par fourchette de prix"""
        try:
            products_data = self.api_client.get_products_by_price_range(min_price, max_price)
            return [Product.from_dict(product_data) for product_data in products_data]
        except Exception as e:
            self.handle_error(e, "récupération des produits par prix")
            return []
    
    def create(self, product_request: CreateProductRequest) -> Optional[Product]:
        """Crée un nouveau produit"""
        try:
            product_data = self.api_client.create_product(product_request.to_dict())
            if product_data:
                self.show_success(f"Produit {product_data['nom']} créé avec succès")
                return Product.from_dict(product_data)
            return None
        except Exception as e:
            self.handle_error(e, "création du produit")
            return None
    
    def update(self, product_id: int, product_request: UpdateProductRequest) -> Optional[Product]:
        """Met à jour un produit"""
        try:
            product_data = self.api_client.update_product(product_id, product_request.to_dict())
            if product_data:
                self.show_success(f"Produit {product_data['nom']} mis à jour avec succès")
                return Product.from_dict(product_data)
            return None
        except Exception as e:
            self.handle_error(e, f"mise à jour du produit {product_id}")
            return None
    
    def delete(self, product_id: int) -> bool:
        """Supprime un produit"""
        try:
            success = self.api_client.delete_product(product_id)
            if success:
                self.show_success(f"Produit {product_id} supprimé avec succès")
            else:
                self.show_warning(f"Impossible de supprimer le produit {product_id}")
            return success
        except Exception as e:
            self.handle_error(e, f"suppression du produit {product_id}")
            return False
    
    def update_stock(self, product_id: int, quantity: int) -> bool:
        """Met à jour le stock d'un produit"""
        try:
            success = self.api_client.update_stock(product_id, quantity)
            if success:
                self.show_success(f"Stock du produit {product_id} mis à jour")
            else:
                self.show_warning(f"Impossible de mettre à jour le stock du produit {product_id}")
            return success
        except Exception as e:
            self.handle_error(e, f"mise à jour du stock du produit {product_id}")
            return False
    
    def get_statistics(self) -> dict:
        """Récupère les statistiques des produits"""
        try:
            all_products = self.get_all()
            in_stock = self.get_in_stock()
            out_of_stock = [p for p in all_products if p.quantite_stock == 0]
            
            # Statistiques par catégorie
            categories = {}
            for product in all_products:
                if product.categorie not in categories:
                    categories[product.categorie] = 0
                categories[product.categorie] += 1
            
            # Valeur totale du stock
            total_value = sum(p.prix * p.quantite_stock for p in all_products)
            
            return {
                "total": len(all_products),
                "in_stock": len(in_stock),
                "out_of_stock": len(out_of_stock),
                "categories": categories,
                "total_value": total_value,
                "products": all_products
            }
        except Exception as e:
            self.handle_error(e, "récupération des statistiques produits")
            return {
                "total": 0, "in_stock": 0, "out_of_stock": 0, 
                "categories": {}, "total_value": 0, "products": []
            }

