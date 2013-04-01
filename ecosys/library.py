from flask import (Blueprint, request, abort, render_template, flash, redirect,
                   url_for)
from flaskext.uploads import configure_uploads
from flask.ext import login as flask_login

from ecosys import forms
from ecosys import auth
from ecosys import plugldap


library = Blueprint('library', __name__)


def initialize_app(app):
    app.register_blueprint(library)
    configure_uploads(app, forms.files)


@library.route('/')
def home():
    if flask_login.current_user.is_anonymous():
        return "not logged in"
    else:
        return "You must be %s" % flask_login.current_user['email']



@library.route('/add/<string:resource_type>', methods=['GET', 'POST'])
@flask_login.login_required
def edit(resource_type):
    try:
        ResourceForm, ReviewForm = forms.FORMS[resource_type]
    except KeyError:
        abort(404)

    resource_form = ResourceForm(resource_type=resource_type)
    review_form = ReviewForm()

    user = flask_login.current_user
    if request.method == 'POST':
        resource_form_validate = resource_form.validate()
        review_form_validate = review_form.validate()
        if resource_form_validate and review_form_validate:
            resource = resource_form.save()
            review_form.save(resource, user)

    return render_template('edit.html', resource_form=resource_form,
                           review_form=review_form)