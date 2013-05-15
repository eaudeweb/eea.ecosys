import requests
from flask import url_for
from flask import current_app as app
from flask.ext.script import Command
from ecosys.models import TaskQueue


class ApiRequest(Command):
    """
    Cron that makes requests to Ecosystem Assessment Virtual Library API for
    indexing
    """

    def run(self):
        api_url = app.config['API_URL']
        for task in TaskQueue.objects.filter(compleated=False):
            resource = task.resource
            url = url_for('library.view', resource_id=str(resource.id),
                          _external=True)
            origin = ','.join(resource.reviews[0].origin)
            import pdb; pdb.set_trace()
            data = {
                'document_type': resource.resource_type,
                'title': resource.title,
                'language': resource.language,
                'english_title': resource.english_title,
                'published_year': resource.year_of_publication,
                'origin': origin,
                'is_final':resource.reviews[0].status,
                'license': '',
                'url': url,
            }
            request = requests.post(api_url, data=data)
            if request.status_code == 200:
                print request.content
                task.compleated = True
                # task.save()
            else:
                print 'Response with status code %s and message %s' % (
                    request.status_code, request.content
                )


