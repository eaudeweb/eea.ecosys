from datetime import datetime

from flask.ext.mongoengine.wtf import model_form
from flask.ext.uploads import UploadSet, AllExcept, SCRIPTS, EXECUTABLES
from flask.ext import wtf
from flask.ext import login as flask_login


from ecosys import models
from ecosys.forms.fields import *
from ecosys.model_data import *


files = UploadSet('files', AllExcept(SCRIPTS + EXECUTABLES))


_LiteratureForm = model_form(models.LiteratureReview)
_LiteratureResourceForm = model_form(models.Resource,
                                     exclude=['organizers', 'reviews'])
_FeedbackForm = model_form(models.Feedback)


class EcosystemType(wtf.Form):

    COLSPAN = 10

    urban = MultiCheckboxField(pre_validate=False)

    cropland = MultiCheckboxField(pre_validate=False)

    grassland = MultiCheckboxField(pre_validate=False)

    woodland = MultiCheckboxField('Woodland & forest', pre_validate=False)

    heathland = MultiCheckboxField('Heathland & shrub', pre_validate=False)

    sparsely_vegetated_land = MultiCheckboxField('Sparsely vegetated land',
                                                 pre_validate=False)

    wetland = MultiCheckboxField(pre_validate=False)

    rivers_lakes = MultiCheckboxField('Rivers & lakes', pre_validate=False)

    marine = MultiCheckboxField(pre_validate=False)


class EcosystemServiceType(wtf.Form):

    COLSPAN = 4

    provisioning = MultiCheckboxField(pre_validate=False)

    regulating = MultiCheckboxField(pre_validate=False)

    cultural = MultiCheckboxField(pre_validate=False)


class LiteratureResourceForm(_LiteratureResourceForm):

    META = {
        'item': 'document',
    }

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
        return resource


class LiteratureForm(_LiteratureForm):

    origin = wtf.SelectMultipleField('Origin of the document',
                                     choices=ORIGIN,
                                     validators=[wtf.validators.Required()])

    origin_other = wtf.TextField(widget=TextInputWithAttributes(attr={
        'data-placeholder': 'or type here different ones'}))

    filename = MultipleFileField('File upload representing the document, if freely available',
        validators=[MultipleFileAllowed(files, 'Document is not valid')])

    spatial = wtf.SelectField('Spatial specificity', choices=YES_NO_DONT_KNOW,
        validators=[
            wtf.validators.Required(),
            RequiredIfChecked(fields=['spatial_scale', 'countries'],
                              message='Spatial scale and Countries are required')
        ])

    url = wtf.TextField()

    ecosystem_types_issues = wtf.FormField(EcosystemType,
        widget=EcosystemTableWidget(data=ECOSYSTEM_ISSUES, categ='Issues',
                        label=('Please indicate which issue(s) and method(s)'
                               ' are addressed per ecosystem type(s)')))

    ecosystem_types_methods = wtf.FormField(EcosystemType,
        widget=EcosystemTableWidget(data=ECOSYSTEM_METHODS, categ='Methods'))

    ecosystem_services_types = wtf.FormField(EcosystemServiceType,
        widget=EcosystemServiceTableWidget(data=ECOSYSTEM_TYPES,
            label=('Please indicate which type(s) of ecosystem services is'
                   ' (are) addressed, per type(s) of ecosystems')))

    content = wtf.SelectMultipleField('Main content or purpose',
                                      choices=CONTENT,
                                      validators=[wtf.validators.Required()])
    content_other = wtf.TextField(widget=TextInputWithAttributes(attr={
        'data-placeholder': 'or type here different ones'}))

    feedback = wtf.SelectField('How did you find out about this resource?',
                               choices=FEEDBACK,
                               validators=[wtf.validators.Required()])
    feedback_other = wtf.TextField(widget=TextInputWithAttributes(attr={
        'data-placeholder': 'or type here different ones'}))

    resource_feedback = wtf.TextAreaField('Optionally, provide your opinion or feedback regarding this resource')

    resource_feedback_files = MultipleFileField('Attach any files you need to complement your feedback on this resource',
        validators=[MultipleFileAllowed(files, 'Document is not valid')])

    def __init__(self, *args, **kwargs):
        super(LiteratureForm, self).__init__(*args, **kwargs)
        self.spatial_scale.flags.required = True
        self.countries.flags.required = True

    def validate_ecosystems(self, field):
        if self.data['ecosystems'] =='Yes':
            values = [v for v in self.data['ecosystem_types_issues'].values()]
            values.extend([v for v in self.data['ecosystem_types_methods'].values()])
            if not any(values):
                raise wtf.validators.ValidationError(
                    'You stated specific ecosystems are addressed. '
                    'It is mandatory you indicate (tick) the addressed issues or '
                    'methods')

    def validate_ecosystem_services(self, field):
        if self.data['ecosystem_services'] == 'Yes':
            values = [v for v in self.data['ecosystem_services_types'].values()]
            if not any(values):
                raise wtf.validators.ValidationError(
                    'You stated specific ecosystems services are addressed. '
                    'It is mandatory you indicate (tick) the addressed types of '
                    'ecosystems')

    def save(self, resource, user):
        review = models.LiteratureReview()

        origin = self.data['origin']
        origin_other = self.data['origin_other'].split(',')
        if origin_other and origin_other[0]:
            origin.extend(origin_other)

        review.origin = self.data['origin']
        review.status = self.data['status']
        review.availability = self.data['availability']
        review.languages = self.data['languages']
        review.url = self.data['url']

        filename_list = self.data['filename']
        if isinstance(filename_list, list) and filename_list:
            review.filename = [files.save(f) for f in filename_list]

        review.spatial = self.data['spatial']
        if review.spatial == 'Yes':
            review.spatial_scale = self.data['spatial_scale']
            review.countries = self.data['countries']

        review.spatial_scale = self.data['spatial_scale']
        review.countries = self.data['countries']
        content =  self.data['content']
        content_other = self.data['content_other'].split(',')
        if content_other:
            content.extend(content_other)
        review.content = content
        review.key_elements = self.data['key_elements']

        feedback = self.data['feedback']
        feedback_other = self.data['feedback_other']
        if feedback_other:
            feedback = feedback_other
        review.feedback = feedback

        review.resource_feedback = self.data['resource_feedback']
        resource_feedback_files_list = self.data['resource_feedback_files']
        if isinstance(resource_feedback_files_list, list):
            review.resource_feedback_files = [files.save(f) for f in resource_feedback_files_list]

        review.ecosystems = self.data['ecosystems']
        if review.ecosystems == 'Yes':
            review.ecosystem_types_issues = self.data['ecosystem_types_issues']
            review.ecosystem_types_methods = self.data['ecosystem_types_methods']

        review.ecosystem_services = self.data['ecosystem_services']
        if review.ecosystem_services == 'Yes':
            review.ecosystem_services_types = self.data['ecosystem_services_types']

        review.user = models.User.objects().get(id=user.id)
        review.datetime = datetime.now()
        resource.reviews.append(review)
        resource.save()


class FeedbackForm(_FeedbackForm):

    description = wtf.TextAreaField('Please provide your feedback')

    files = MultipleFileField(
        'You can also attach screenshots or other files related to your feedback',
        validators=[MultipleFileAllowed(files, 'Document is not valid')])

    def save(self):
        if self.data['description']:
            user = models.User.objects().get(id=flask_login.current_user.id)
            feedback = models.Feedback(user=user)
            feedback.description = self.data['description']
            file_list = self.data['files']
            if isinstance(file_list, list):
                feedback.files = [files.save(f) for f in file_list]
            feedback.save()
            return feedback


FORMS= {
    'literature': (LiteratureResourceForm, LiteratureForm),
}

