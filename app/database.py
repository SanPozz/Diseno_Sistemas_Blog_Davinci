from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
