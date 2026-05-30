import app.database as db

from app.models.Categories import Category

class CategoryRepository:
    @staticmethod
    def get_all():
        return Category.query.all()
    
    @staticmethod
    def get_by_id(category_id):
        return Category.query.get(category_id)
    
    @staticmethod
    def create(category):
        db.session.add(category)
        db.session.commit()
        return category