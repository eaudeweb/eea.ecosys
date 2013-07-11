from flask import (Blueprint, request, abort, render_template, flash, redirect,
                   url_for, views, g, jsonify)
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


class Edit(views.MethodView):

    def _get_instance_form(self, resource_type, data=None):
        try:
            ResourceForm, ReviewForm = forms.FORMS[resource_type]
        except KeyError:
            abort(404)

        if data:
            resource_form = ResourceForm(data, resource_type=resource_type)
            review_form = ReviewForm(data)
        else:
            resource_form = ResourceForm(resource_type=resource_type)
            review_form = ReviewForm()
        return resource_form, review_form

    def get(self, resource_type):
        resource_form, review_form = self._get_instance_form(resource_type)
        user = flask_login.current_user
        if not user.is_anonymous() and not user.country:
            next_url = url_for('.edit', resource_type=resource_type)
            return redirect(url_for('auth.profile', next=next_url))
        return render_template('edit.html', resource_form=resource_form,
                               review_form=review_form)

    @flask_login.login_required
    def post(self, resource_type):
        data = request.form.copy()
        data.update(request.files)

        resource_form, review_form = self._get_instance_form(resource_type, data)
        user = flask_login.current_user

        resource_form_validate = resource_form.validate()
        review_form_validate = review_form.validate()

        if resource_form_validate and review_form_validate:
            resource = resource_form.save()
            review_form.save(resource, user)
            flash('Resource added successfully', 'success')
            return redirect(url_for('.feedback'))
        else:
            message = ('You have required fields unfilled. '
                        'Please correct the errors and resubmit.')
            if request.files:
                message = (('%s You will need to re-select the file '
                            'for upload') % message)
            flash(message, 'error')

        return render_template('edit.html', resource_form=resource_form,
                               review_form=review_form)

library.add_url_rule('/resources/add/<string:resource_type>',
                     view_func=Edit.as_view('edit'))


@library.route('/resources')
@library.route('/resources/me', defaults={'filter_by': 'me'})
@flask_login.login_required
def resources(filter_by=None):
    user = flask_login.current_user
    resources = Resource.objects
    if filter_by == 'me':
        resources = resources.filter(reviews__match={'user.$id': user.id})
    return render_template('resources.html', resources=resources,
                           filter_by=filter_by)


class Feedback(views.MethodView):

    decorators = (flask_login.login_required,)

    def get(self):
        form = forms.FeedbackForm()
        return render_template('feedback.html', form=form)

    def post(self):
        form = forms.FeedbackForm()
        if form.validate():
            form.save()
            flash('Thanks for the feedback', 'success')
            return redirect(url_for('.resources'))
        return render_template('feedback.html', form=form)

library.add_url_rule('/feedback', view_func=Feedback.as_view('feedback'))


@library.route('/resource/<string:resource_id>')
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


@library.route('/resource/<string:resource_id>', methods=['DELETE'])
@flask_login.login_required
def delete(resource_id):
    resource = Resource.objects.get_or_404(id=resource_id)
    user = flask_login.current_user
    if user.has_delete_role(resource):
        resource.delete()
        return jsonify({'url': url_for('.resources')})
    else:
        abort(401)
