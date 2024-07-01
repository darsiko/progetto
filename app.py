from index import index_blueprint
from models import login_manager, User, app
from register import register_blueprint
from login import login_blueprint
from error import error_pages_blueprint
from products import products_blueprint
from admin import admin_blueprint
from cart import cart_blueprint
from private_area import private_area_blueprint
from users import users_blueprint
from review import review_blueprint
from orders import orders_blueprint


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        print(e)
        return None


app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(error_pages_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(products_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(cart_blueprint)
app.register_blueprint(orders_blueprint)
app.register_blueprint(private_area_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(review_blueprint)
app.register_blueprint(orders_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
