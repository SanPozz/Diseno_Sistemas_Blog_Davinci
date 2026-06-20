from flask_sqlalchemy import SQLAlchemy


class SingletonMeta(type):
    """garantiza una única instancia de SQLAlchemy."""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseManager(SQLAlchemy, metaclass=SingletonMeta):
    """Wrapper singleton para SQLAlchemy que garantiza una única instancia."""
    pass


# Instancia singleton de la base de datos
db = DatabaseManager()


def init_db(app):

    db.init_app(app)

    with app.app_context():
        from app.models.Users import User
        from app.models.Posts import Post
        from app.models.Comments import Comment
        from app.models.Categories import Category

        db.create_all()

        # creamos categorias por defecto
        default_categories = ["Videojuegos", "Cine", "Futbol"]

        for category_name in default_categories:

            existing_category = Category.query.filter_by(name=category_name).first()

            if not existing_category:

                category = Category(name=category_name)

                db.session.add(category)

        db.session.commit()

        print("Base de datos creada!")
