from flask.ext.mongoengine.wtf import model_form
from flask.ext import wtf
from flask.ext.uploads import UploadSet, AllExcept, SCRIPTS, EXECUTABLES

from ecosys import models
from ecosys.model_data import *


files = UploadSet('files', AllExcept(SCRIPTS + EXECUTABLES))


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

        required_flag = wtf.Flags()
        required_flag.required = True

        self.resource_type.data = resource_type
        self.authors.validators = [wtf.validators.Required()]
        self.authors.flags = required_flag
        self.organisations.validators = [wtf.validators.Required()]
        self.organisations.flags = required_flag
        self.year_of_publication.validators = [wtf.validators.Required()]
        self.year_of_publication.flags = required_flag

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
    origin_other = wtf.TextField()

    filename = CustomFileField('File upload representing the document, if freely available',
       validators=[wtf.file_allowed(files, 'Document is not valid')])

    spatial = CustomBoolean('Spatial specificity', choices=YES_NO, default='0',
        validators=[RequiredIfChecked(fields=['spatial_scale', 'countries'],
                                      message='Spatial scale and Countries are required')])

    content = wtf.SelectMultipleField('Main content or purpose: mutliple select',
                                      choices=CONTENT,
                                      validators=[wtf.validators.Required()])
    content_other = wtf.TextField()

    feedback = wtf.SelectField('How did you came to know this document?',
                               choices=FEEDBACK,
                               validators=[wtf.validators.Required()])
    feedback_other = wtf.TextField()

    def __init__(self, *args, **kwargs):
        super(LiteratureForm, self).__init__(*args, **kwargs)


    def save(self, resource):
        review = models.LiteratureReview()

        origin = self.data['origin']
        origin_other = self.data['origin_other'].split(',')
        if origin_other:
            origin.extend(origin_other)

        review.origin = self.data['origin']
        review.status = self.data['status']
        review.availability = self.data['availability']
        review.languages = self.data['languages']
        review.url = self.data['url']

        filename = self.data['filename']
        file_saved = files.save(filename) if filename else ''
        review.filename = file_saved

        import pdb; pdb.set_trace()

        spatial = True if self.data['spatial'] == '1' else False
        review.spatial = spatial

        if int(review.spatial):
            review.spatial_scale = self.data['spatial_scale']
            review.countries = self.data['countries']

        review.spatial_scale = self.data['spatial_scale']
        review.countries = self.data['countries']
        review.content = self.data['content']
        review.key_elements = self.data['key_elements']

        feedback = self.data['feedback']
        feedback_other = self.data['feedback_other']
        if feedback_other:
            feedback = feedback_other
        review.feedback = feedback

        resource.reviews.append(review)
        resource.save()


FORMS= {
    'literature': (LiteratureResourceForm, LiteratureForm),
}

