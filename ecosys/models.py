from datetime import datetime

from flask.ext.mongoengine import MongoEngine
from flask.ext.login import UserMixin
from mongoengine import signals
from werkzeug.utils import cached_property

from ecosys.model_data import *


db = MongoEngine()


class Country(db.Document):

    code = db.StringField(max_length=3, required=True, primary_key=True)

    name = db.StringField(max_length=128, required=True)

    categories = db.ListField(db.StringField(max_length=128), default=None)

    def __unicode__(self):
        return self.name


class User(db.Document, UserMixin):

    id = db.StringField(max_length=16, required=True, primary_key=True)

    first_name = db.StringField(max_length=128, required=True)

    last_name = db.StringField(max_length=128, required=True)

    email = db.StringField(max_length=128, required=True)

    phone_number = db.StringField(max_length=32)

    organisation = db.StringField(max_length=128)

    phone_number = db.StringField(max_length=32)

    last_login = db.DateTimeField()

    country = db.StringField(max_length=3)

    field_of_expertise = db.StringField(max_length=128)

    organisation_type = db.ListField(db.StringField(), default=[])

    roles = db.ListField(db.StringField(choices=ROLES, verbose_name='Roles'),
                         default=[])

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def has_delete_role(self, resource):
        if 'administrator' in self.roles or resource.user == self:
            return True
        return False

    def is_admin(self):
        return True if 'administrator' in self.roles else False


class ReviewMixin():

    user = db.ReferenceField(User)

    datetime = db.DateTimeField()


class Author(db.Document):

    first_name = db.StringField(max_length=128)

    last_name = db.StringField(max_length=128, required=True)

    name = db.StringField(max_length=128, default=None)

    def __unicode__(self):
        if self.last_name and self.first_name:
            return '%s, %s' % (self.last_name, self.first_name)
        return self.last_name


class Organisation(db.Document):

    name = db.StringField(max_length=128, required=True)

    def __unicode__(self):
        return self.name


class Organizer(db.Document):

    name = db.StringField(max_length=128, required=True)

    def __unicode__(self):
        return self.name


class EcosystemCategory(db.EmbeddedDocument):

    provisioning = db.ListField(db.StringField())

    regulating = db.ListField(db.StringField())

    cultural = db.ListField(db.StringField())


class Resource(db.Document):

    title = db.StringField(max_length=512, required=True,
        verbose_name='Title in original language')

    english_title = db.StringField(max_length=512)

    language = db.StringField(choices=LANGUAGES, required=True,
                              verbose_name='Original language', default='EN')

    resource_type = db.StringField(max_length=20, required=True,
                                   choices=RESOURCE_TYPES)

    authors = db.ListField(db.ReferenceField(Author), default=None)

    organisations = db.ListField(db.ReferenceField(Organisation), default=None)

    organizers = db.ListField(db.ReferenceField(Organizer), default=None)

    year_of_publication = db.IntField(min_value=0, default=None)

    reviews = db.ListField(db.GenericEmbeddedDocumentField())

    @cached_property
    def language_verbose(self):
        return dict(LANGUAGES).get(self.language, None)

    @property
    def resource_type_verbose(self):
        return dict(RESOURCE_TYPES).get(self.resource_type, None)

    @cached_property
    def user(self):
        if self.reviews:
            return self.reviews[0].user
        return None


class LiteratureReview(db.EmbeddedDocument, ReviewMixin):

    origin = db.ListField(db.StringField(), required=True,
        verbose_name='Origin of document')

    status = db.StringField(choices=STATUS, required=True,
        verbose_name='What is the status of the document?')

    availability = db.StringField(max_length=20, choices=AVAILABILITY,
        required=True, verbose_name='Is the document freely available?')

    languages = db.ListField(db.StringField(choices=LANGUAGES), default=None,
        verbose_name='In which languages is the document available?')

    url = db.StringField(default=None, verbose_name='URL')

    filename = db.ListField(db.StringField(max_length=128), default=None)

    spatial = db.StringField(choices=YES_NO_DONT_KNOW, required=True,)

    spatial_scale = db.ListField(
        db.StringField(max_length=128, choices=SPATIAL_SCALE), default=None,
        verbose_name='Spatial scale')

    countries = db.ListField(db.ReferenceField(Country),
        default=None, verbose_name="Countries in Europe")

    content = db.ListField(db.StringField(), required=True)

    key_elements = db.ListField(db.StringField(choices=KEY_ELEMENTS),
        required=True, verbose_name='Which key elements of ecosystem assessment are documented? ')

    ecosystems = db.StringField(choices=YES_NO_DONT_KNOW, required=True,
        verbose_name='Are there any <u>specific</u> ecosystems addressed in the document?')

    ecosystem_types_issues = db.DictField(default=None)

    ecosystem_types_methods = db.DictField(default=None)

    ecosystem_services = db.StringField(choices=YES_NO_DONT_KNOW, required=True,
        verbose_name='Are there any <u>specific</u> ecosystem services addressed in the document?')

    ecosystem_services_types = db.DictField(default=None)

    feedback = db.StringField(default=None)

    resource_feedback = db.StringField(default=None)

    resource_feedback_files = db.ListField(db.StringField(max_length=128), default=None)

    @cached_property
    def languages_verbose(self):
        languages = dict(LANGUAGES)
        return [languages.get(l) for l in self.languages]

    @cached_property
    def countries_verbose(self):
        return [c.name for c in self.countries]


class EcosystemType(db.EmbeddedDocument):

    urban = db.ListField(db.StringField())

    cropland = db.ListField(db.StringField())

    grassland = db.ListField(db.StringField())

    woodland = db.ListField(db.StringField())

    heathland = db.ListField(db.StringField())

    sparsely_vegetated_land = db.ListField(db.StringField())

    wetland = db.ListField(db.StringField())

    rivers_lakes = db.ListField(db.StringField())

    marine = db.ListField(db.StringField())


class EcosystemCategory(db.EmbeddedDocument):

    provisioning = db.ListField(db.StringField())

    regulating = db.ListField(db.StringField())

    cultural = db.ListField(db.StringField())


class Feedback(db.Document):

    user = db.ReferenceField(User)

    description = db.StringField(default=None)

    files = db.ListField(db.StringField(max_length=128), default=[])

    date = db.DateTimeField()

    def __unicode__(self):
        return u'%s' % self.user


class TaskQueue(db.Document):

    resource = db.ReferenceField(Resource, primary_key=True)

    action = db.StringField(max_length=64)

    date = db.DateTimeField()

    completed = db.BooleanField(default=False)

    def __unicode__(self):
        return u'%s - %s' % (self.resource.id, self.action)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        created = kwargs.get('created', False)
        if created:
            task_queue = cls.objects.create(
                resource=document,
                action='post',
                date=datetime.now())

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        task_queue = cls.objects.create(
                resource=document,
                action='delete',
                date=datetime.now())


signals.post_save.connect(TaskQueue.post_save, sender=Resource)
signals.post_delete.connect(TaskQueue.post_delete, sender=Resource)
