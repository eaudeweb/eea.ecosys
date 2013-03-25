from flask.ext.mongoengine.wtf import model_form
from flask.ext import wtf

from ecosys import models
from ecosys.model_data import *


class CustomBoolean(wtf.SelectField):

    def process_data(self, value):
        self.data = (value == '1')


class CustomFileField(wtf.FileField):

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            filestorage = valuelist[0]
            filestorage.filename = filestorage.filename.lower()
            self.data = filestorage
        else:
            self.data = ''


class RequiredIfChecked(object):

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message or '%s are required' % (', '.join(fields))

    def __call__(self, form, field):
        if field.data == '0':
            return True
        for f in self.fields:
            required_field = getattr(form, f, None)
            if required_field and required_field.data:
                continue
            else:
                raise wtf.ValidationError(self.message)


_LiteratureForm = model_form(models.LiteratureReview)
_LiteratureResourceForm = model_form(models.Resource,
                                     exclude=['organizers', 'reviews'])


class LiteratureResourceForm(_LiteratureResourceForm):

    def __init__(self, *args, **kwargs):
        resource_type = kwargs.pop('resource_type')
        super(LiteratureResourceForm, self).__init__(*args, **kwargs)

        self.resource_type.data = resource_type
        self.authors.validators = [wtf.validators.Required()]
        self.organisations.validators = [wtf.validators.Required()]
        self.year_of_publication.validators = [wtf.validators.Required()]

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

    origin = wtf.SelectMultipleField('Origin of the document',
                                     choices=ORIGIN,
                                     validators=[wtf.validators.Required()])

    filename = CustomFileField('File upload representing the document, if freely available')

    spatial = CustomBoolean('Spatial specificity', choices=YES_NO, default='0',
        validators=[RequiredIfChecked(fields=['spatial_scale', 'countries'],
                                      message='Spatial scale and Countries are required')])

    content = wtf.SelectMultipleField('Main content or purpose: mutliple select',
                                      choices=CONTENT,
                                      validators=[wtf.validators.Required()])

    def __init__(self, *args, **kwargs):
        super(LiteratureForm, self).__init__(*args, **kwargs)

    def save(self, resource):
        review = models.LiteratureReview()
        review.origin = self.data['origin']
        review.status = self.data['status']
        review.availability = self.data['availability']
        review.languages = self.data['languages']
        review.url = self.data['url']

        spatial = True if self.data['spatial'] == '1' else False
        review.spatial = spatial

        if int(review.spatial):
            review.spatial_scale = self.data['spatial_scale']
            review.countries = self.data['countries']

        review.spatial_scale = self.data['spatial_scale']
        review.countries = self.data['countries']
        review.content = self.data['content']
        review.key_elements = self.data['key_elements']

        resource.reviews.append(review)
        resource.save()


FORMS= {
    'literature': (LiteratureResourceForm, LiteratureForm),
}

