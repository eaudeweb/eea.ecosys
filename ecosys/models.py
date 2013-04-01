from flask.ext.mongoengine import MongoEngine
from flask.ext.login import UserMixin

from ecosys.model_data import *


db = MongoEngine()


class User(db.Document, UserMixin):

    id = db.StringField(max_length=16, required=True, primary_key=True)

    first_name = db.StringField(max_length=128, required=True)

    last_name = db.StringField(max_length=128, required=True)

    email = db.StringField(max_length=128, required=True)

    phone_number = db.StringField(max_length=32)

    organisation = db.StringField(max_length=128)

    last_login = db.DateTimeField()

    def get_id(self):
        return self.id

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)


class ReviewMixin():

    user = db.ReferenceField(User)

    datetime = db.DateTimeField()


class Author(db.Document):

    name = db.StringField(max_length=128, required=True)

    def __unicode__(self):
        return self.name


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

    title = db.StringField(max_length=512, required=True)

    english_title = db.StringField(max_length=512)

    language = db.StringField(choices=LANGUAGES, required=True,
                              verbose_name='Original language')

    resource_type = db.StringField(max_length=20, required=True,
                                   choices=RESOURCE_TYPES)

    authors = db.ListField(db.ReferenceField(Author), default=None)

    organisations = db.ListField(db.ReferenceField(Organisation), default=None)

    organizers = db.ListField(db.ReferenceField(Organizer), default=None)

    year_of_publication = db.IntField(min_value=0, default=None)

    reviews = db.ListField(db.GenericEmbeddedDocumentField())

    @property
    def language_verbose(self):
        return dict(LANGUAGES).get(self.language, None)

    @property
    def resource_type_verbose(self):
        return dict(RESOURCE_TYPES).get(self.resource_type, None)


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

    filename = db.StringField(max_length=128, default=None)

    spatial = db.BooleanField(default=False)

    spatial_scale = db.ListField(
        db.StringField(max_length=128, choices=SPATIAL_SCALE), default=None,
        verbose_name='Spatial scale')

    countries = db.ListField(
        db.StringField(max_length=128, choices=COUNTRIES),
        default=None)

    content = db.ListField(db.StringField(), required=True)

    key_elements = db.ListField(db.StringField(choices=KEY_ELEMENTS),
        required=True, verbose_name='Which key elements of ecosystem assessment are documented? ')

    ecosystems = db.BooleanField(default=False)

    ecosystem_types_issues = db.DictField(default=None)

    ecosystem_types_methods = db.DictField(default=None)

    ecosystem_services = db.BooleanField(default=False)

    ecosystem_services_types = db.DictField(default=None)

    feedback = db.StringField(default=None)


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
