import os
from flask import Flask, Blueprint, g
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import Config
from app.models import db

migrate = Migrate()
url = 'mysql://webdep:M4k3SqlLabGreatAg4in@localhost:3306/voting_system'
engine = db.create_engine(url)
debug = True

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=url
    )
    app.config.from_object(Config)

    # initialize the database
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        if debug:
            db.drop_all()
        db.create_all()

    # register blueprints
    from app.routes.polls import polls
    app.register_blueprint(polls, url_prefix='/api')
    from app.routes.auth import auth
    app.register_blueprint(auth, url_prefix='/api')
    from app.routes.admin import admin
    app.register_blueprint(admin, url_prefix='/api')

    CORS(app, resources={r"/*": {"origins": "*"}})

    # public folders
    @app.route('/', methods=['GET'])
    def index():
        return "Success"

    return app
