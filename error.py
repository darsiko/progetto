from flask import Blueprint, render_template

error_pages_blueprint = Blueprint("error_pages", __name__, template_folder="templates", static_folder='static')


@error_pages_blueprint.app_errorhandler(404)
def error_404():
    return render_template("404.html"), 404


@error_pages_blueprint.app_errorhandler(403)
def error_403():
    return render_template("403.html"), 403
