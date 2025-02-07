import os

from flask import Flask, jsonify
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))
# Constantes
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = os.environ["POSTGRES_HOST"]
DB_PORT = os.environ["POSTGRES_PORT"]
DB_NAME =  os.environ["POSTGRES_DB"]

def registrar_handlers():
    import modulos.companias.aplicacion


def importar_modelos_alchemy():
    import modulos.companias.infraestructura.dto

def comenzar_consumidor():
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """

    import threading
    import modulos.companias.infraestructura.consumidores as companias

    # Suscripción a eventos
    threading.Thread(target=companias.suscribirse_a_eventos).start()
    threading.Thread(target=companias.suscribirse_a_eventos_eliminada).start()


    # Suscripción a comandos
    threading.Thread(target=companias.suscribirse_a_comandos).start()
    threading.Thread(target=companias.suscribirse_a_comandos_eliminada).start()


def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from config.db import init_db
    init_db(app)

    from config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor()

     # Importa Blueprints
    from . import recursos

    # Registro de Blueprints
    app.register_blueprint(recursos.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app