from flask import (Blueprint, request, abort, render_template, flash, redirect,
                   url_for)
from flaskext.uploads import configure_uploads
from flask.ext.login import current_user, login_required, login_user
from ecosys import forms
from ecosys import auth


library = Blueprint('library', __name__)


def initialize_app(app):
    app.register_blueprint(library)
    configure_uploads(app, forms.files)


@library.route('/')
@login_required
def home():
    return current_user['email']


@library.route("/login", methods=["GET", "POST"])
def login():
    form = auth.LoginForm()
    if form.validate_on_submit():
        user = auth.login_user(request.form['username'],
                               request.form['password'])
        if user:
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for(".home"))
    return render_template("login.html", form=form)


@library.route('/add/<string:resource_type>', methods=['GET', 'POST'])
def edit(resource_type):
    try:
        ResourceForm, ReviewForm = forms.FORMS[resource_type]
    except KeyError:
        abort(404)

    resource_form = ResourceForm(resource_type=resource_type)
    review_form = ReviewForm()

    if request.method == 'POST':
        resource_form_validate = resource_form.validate()
        review_form_validate = review_form.validate()
        if resource_form_validate and review_form_validate:
            resource = resource_form.save()
            review_form.save(resource)

    return render_template('edit.html', resource_form=resource_form,
                           review_form=review_form)