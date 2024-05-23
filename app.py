from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ubersecret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/e_commerce'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from register.register import register_bp
    from login.login import login_bp
    from login_admin.login_Admin import login_admin_bp
    from home.home import home_bp
    from products.products import products_bp

    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(login_admin_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(products_bp)

    @app.route("/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods:
                try:
                    url = url_for(rule.endpoint, **(rule.defaults or {}))
                    links.append((url, rule.endpoint))
                except:
                    pass
        return links

    return app


if __name__ == '__main__':
    app = create_app()
    print(app.url_map)
    app.run(debug=True)
