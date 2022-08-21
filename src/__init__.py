from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testsecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    create_database(app)

    from .views import views
    from .auth import auth
    from .comments import comments
    from .backend import backend
    app.register_blueprint(backend, url_prefix='/admin')
    app.register_blueprint(comments, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .model import Users

    @login_manager.user_loader
    def load_user(key):
        return Users.query.get(int(key))

    return app

def create_database(app):
    if not path.exists('./' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')