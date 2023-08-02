from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from webapp.core.models import User
    from webapp.pizza.models import Topping, Pizza

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from webapp.core.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from webapp.core.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from webapp.pizza.views import pizza as pizza_blueprint
    app.register_blueprint(pizza_blueprint)

    return app
