from flask.ext.mongoengine.wtf import model_form
from flask.ext import wtf

from ecosys import models, model_data


class CustomFileField(wtf.FileField):

    def process_formdata(self, valuelist):
        if valuelist:
            filestorage = valuelist[0]
            filestorage.filename = filestorage.filename.lower()
            self.data = filestorage
        else:
            self.data = ''


_LiteratureForm = model_form(models.LiteratureReview)
_LiteratureResourceForm = model_form(models.Resource,
                                     exclude=['organizers', 'reviews'])


class LiteratureResourceForm(_LiteratureResourceForm):

    def __init__(self, *args, **kwargs):
        resource_type = kwargs.pop('resource_type')
        super(LiteratureResourceForm, self).__init__(*args, **kwargs)
        self.resource_type.data = resource_type

    def save(self):
        resource = models.Resource()
        resource.title = self.data['title']
        resource.english_title = self.data['english_title']
        resource.language = self.data['language']
        resource.resource_type = self.data['resource_type']
        resource.authors = self.data['authors']
        resource.organisations = self.data['organisations']
        resource.year_of_publication = self.data['year_of_publication']
        resource.reviews = []
        return resource.save()


class LiteratureForm(_LiteratureForm):

    origin = wtf.SelectMultipleField('Origin of the document')

    filename = CustomFileField('File upload representing the document, if freely available')

    content = wtf.SelectMultipleField('Main content or purpose: mutliple select')

    def __init__(self, *args, **kwargs):
        super(LiteratureForm, self).__init__(*args, **kwargs)
        self.origin.choices = model_data.ORIGIN
        self.content.choices = model_data.CONTENT

    def save(self, resource):
        pass


FORMS= {
    'literature': (LiteratureResourceForm, LiteratureForm),
}

