from flask import Blueprint, render_template

from models import Review

review_blueprint = Blueprint('review_blueprint', __name__, template_folder='templates', static_folder='static')


@review_blueprint.route('/<int:idx>/review', methods=['GET', 'POST'])
def review(idx):
    rev = Review.query.filter_by(product_id=idx)
    return render_template('review.html', review=rev)


@review_blueprint.route('/<int:idx>/add_review', methods=['GET', 'POST'])
def add_review(idx):
    return render_template('add_review.html')
