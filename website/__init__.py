from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2Vp32v9du23S8#dy0-a*sd3'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
