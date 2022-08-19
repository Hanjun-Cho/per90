from flask import Flask

app = Flask(__name__)
domain = "localhost:5000/"

def create_app():
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app