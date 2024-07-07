from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from form import ReviewForm
from models import Review, Product, db, User
from datetime import date

review_blueprint = Blueprint('review_blueprint', __name__, template_folder='templates', static_folder='static')


@review_blueprint.route('/<int:idx>/review', methods=['GET', 'POST'])
def review(idx):
    rev = Review.query.filter_by(product_id=idx)
    prod = Product.query.filter_by(id=idx).first()
    return render_template('review.html', review=rev, product=prod)


@review_blueprint.route('/<int:idx>/add_review', methods=['GET', 'POST'])
def add_review(idx):
    form = ReviewForm()
    if form.validate_on_submit():
        rev = Review(score=form.score.data, text=form.text.data, date=date.today(), product_id=idx,
                     user_id=current_user.id)
        db.session.add(rev)
        db.session.commit()
        return redirect(url_for('review_blueprint.review', idx=idx))
    return render_template('add_review.html', form=form)
