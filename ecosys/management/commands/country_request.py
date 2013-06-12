import requests
import sparql

from flask import current_app as app
from flask.ext.script import Command

from ecosys.models import Country


class CountryRequest(Command):

    """
    Cron that updates country membership.
    """

    def run(self):
        s = sparql.Service(app.config['SPARQL_ENDPOINT'])
        query_path = app.config['ROOT_PATH'] / 'sparql' / 'country_query.sparql'
        query = query_path.text()

        results = [i for i in s.query(query).fetchone()]
        if len(results) > 0:
            for item in results:
                (code, name, pub_code, eu, eea, eionet, eun22) = item
                country, created = Country.objects.get_or_create(
                    code=code.value, defaults={'name': name.value})
                country.categories = country.categories or []
                if eu.value == 'Yes':
                    country.categories.append('eu')
                if eea.value == 'Yes':
                    country.categories.append('eea')
                if eionet.value == 'Yes':
                    country.categories.append('eionet')
                if eun22.value == 'Yes':
                    country.categories.append('eun22')
                country.save()
        else:
            print 'Empty dataset'
