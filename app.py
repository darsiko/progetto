from register import register_bp
from login import login_bp
from login_Admin import login_admin_bp
from home import home_bp
from products import products_bp
from cart import cart_bp
from private import private_bp
from logout import logout_bp

from models import login_manager, User, app


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(login_admin_bp)
app.register_blueprint(home_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(private_bp)
app.register_blueprint(logout_bp)

if __name__ == '__main__':
    app.run(debug=True)
