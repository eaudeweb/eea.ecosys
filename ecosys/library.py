from flask import (Blueprint, request, abort, render_template, flash, redirect,
                   url_for)
from flaskext.uploads import configure_uploads
from flask.ext import login as flask_login

from ecosys import forms, auth, plugldap
from ecosys.models import Resource


library = Blueprint('library', __name__)


def initialize_app(app):
    app.register_blueprint(library)
    configure_uploads(app, forms.files)


@library.route('/')
def home():
    if flask_login.current_user.is_anonymous():
        pass
    else:
        pass
    return render_template('home.html')


@library.route('/resources/add/<string:resource_type>',
               methods=['GET', 'POST'])
@flask_login.login_required
#@auth.requires_role('contributor')
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
            flash('Resource added successfully')

    return render_template('edit.html', resource_form=resource_form,
                           review_form=review_form)


@library.route('/resources')
@flask_login.login_required
def resources():
    resources = Resource.objects
    return render_template('resources.html', resources=resources)


@library.route('/resource/<string:resource_id>')
#@flask_login.login_required
def view(resource_id):
    resource = Resource.objects.get_or_404(id=resource_id)
    try:
        ResourceForm, ReviewForm = forms.FORMS[resource.resource_type]
    except KeyError:
        abort(404)

    resource_form = ResourceForm(resource_type=resource.resource_type)
    review_form = ReviewForm()

    return render_template('view.html', resource=resource,
                           resource_form=resource_form,
                           review_form=review_form)
