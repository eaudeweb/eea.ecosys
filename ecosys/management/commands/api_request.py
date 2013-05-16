import requests
import json
from flask import url_for
from flask import current_app as app
from flask.ext.script import Command
from ecosys.models import TaskQueue, Resource


class ApiRequest(Command):
    """
    Cron that makes requests to Ecosystem Assessment Virtual Library API for
    indexing
    """

    def run(self):
        api_url = app.config['API_URL']
        for task in TaskQueue.objects.filter(completed=False):
            if task.action == 'post':
                resource = task.resource

                url = url_for('library.view', resource_id=str(resource.id),
                              _external=True)
                origin = ','.join(resource.reviews[0].origin)
                status = 'true' if resource.reviews[0].status == 'Final' else 'false'
                status = 'true' # api bug
                data = {
                    'ecosystem_assessment': {
                        'document_type': resource.resource_type,
                        'title': resource.title,
                        'language': resource.language.lower(),
                        'english_title': resource.english_title or resource.title,
                        'published_year': resource.year_of_publication,
                        'origin': origin,
                        'is_final': status,
                        'license': '',
                        'url': url,
                    }
                }
            request = requests.post(api_url, data=json.dumps(data),
                headers={'Content-Type': 'application/json'})
            if request.status_code == 200:
                task.completed = True
                task.save()
            else:
                print 'Response with status code %s and message %s' % (
                    request.status_code, request.content
                )


