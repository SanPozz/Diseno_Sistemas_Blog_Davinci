from flask_sqlalchemy import SQLAlchemy;

db = SQLAlchemy();

def init_db(app):
    db.init_app(app);

    with app.app_context():

        # importar modelos

        db.create_all();
        
        print("Base de datos creada!");