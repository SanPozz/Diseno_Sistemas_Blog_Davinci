from flask import Flask

from config import DevConfig;
from app.database import init_db;

def create_app():

    app = Flask(__name__);

    app.config.from_object(DevConfig);

    init_db(app);

    # Importar blueprints y registrarlos

    return app;