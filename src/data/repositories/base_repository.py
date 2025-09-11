"""
Repository de base avec les opérations CRUD communes
"""

from typing import List, Optional
from ...data.database.db import db


class BaseRepository:
    """Repository de base avec les opérations CRUD communes"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_all(self) -> List:
        """Récupère tous les enregistrements"""
        return self.model_class.query.all()
    
    def get_by_id(self, id: int):
        """Récupère un enregistrement par son ID"""
        return self.model_class.query.get(id)
    
    def create(self, **kwargs):
        """Crée un nouvel enregistrement"""
        instance = self.model_class(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def update(self, id: int, **kwargs):
        """Met à jour un enregistrement"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            db.session.commit()
            return instance
        return None
    
    def delete(self, id: int) -> bool:
        """Supprime un enregistrement"""
        instance = self.get_by_id(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False

