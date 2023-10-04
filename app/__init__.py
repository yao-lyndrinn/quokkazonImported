from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .wishlist import bp as wishes_bp
    app.register_blueprint(wishes_bp)

    from .sellerfeedback import bp as sfeedback_bp
    app.register_blueprint(sfeedback_bp)

    from .productfeedback import bp as pfeedback_bp
    app.register_blueprint(pfeedback_bp)

    from .allpurchases import bp as allpurchases_bp
    app.register_blueprint(allpurchases_bp)

    from .inventory import bp as inventory_bp
    app.register_blueprint(inventory_bp)

    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    return app
