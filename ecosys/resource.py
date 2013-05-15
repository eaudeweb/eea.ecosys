from flask import (Blueprint, request, render_template, jsonify, views, jsonify)
from ecosys import models, forms


resource = Blueprint('resource', __name__)


def initialize_app(app):
    app.register_blueprint(resource)


@resource.route('/author/new', methods=['GET', 'POST'])
def edit_author():
    form = forms.AuthorForm()
    response = {}
    response['status'] = 'error'

    if request.method == 'POST':
        if form.validate():
            author = form.save()
            response['status'] = 'success'
            response['author'] = {'id': str(author.id), 'name': author.name}
        else:
            response['html'] = render_template('author.html', form=form)
    else:
        response['html'] = render_template('author.html', form=form)

    return jsonify(response)


@resource.route('/organization/new', methods=['GET', 'POST'])
def edit_organisation():
    form = forms.OrganisationForm()
    response = {}
    response['status'] = 'error'

    if request.method == 'POST':
        if form.validate():
            organisation = form.save()
            response['status'] = 'success'
            response['organisation'] = {
                'id': str(organisation.id),
                'name': organisation.name
            }
        else:
            response['html'] = render_template('organisation.html', form=form)
    else:
        response['html'] = render_template('organisation.html', form=form)

    return jsonify(response)


class ApiTest(views.MethodView):

    def get(self):
        return ''

    def post(self):
        return jsonify(request.form.to_dict())

resource.add_url_rule('/api/test', view_func=ApiTest.as_view('api_test'))

