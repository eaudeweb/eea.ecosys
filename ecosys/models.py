from flask.ext.mongoengine import MongoEngine
from ecosys.model_data import *

db = MongoEngine()


class Authors(db.Document):

    name = db.StringField(max_length=128, required=True)

    def __unicode__(self):
        return self.name


class Organisations(db.Document):

    name = db.StringField(max_length=128, required=True)


class Organizers(db.Document):

    name = db.StringField(max_length=128, required=True)



class Resource(db.Document):

    title = db.StringField(max_length=512, required=True)

    english_title = db.StringField(max_length=512)

    language = db.StringField(choices=LANGUAGES, required=True,
                              verbose_name='Original language')

    resource_type = db.StringField(max_length=20, required=True,
                                   choices=RESOURCE_TYPES)

    authors = db.ListField(db.ReferenceField(Authors), default=None)

    organisations = db.ListField(db.ReferenceField(Organisations), default=None)

    organizers = db.ListField(db.ReferenceField(Organizers), default=None)

    year_of_publication = db.IntField(min_value=0, default=None)

    reviews = db.ListField(db.GenericEmbeddedDocumentField())



class LiteratureReview(db.EmbeddedDocument):

    origin = db.ListField(db.StringField(), default=None,
        verbose_name='Origin of document')

    status = db.StringField(choices=STATUS, default=None,
        verbose_name='What is the status of the document?')

    availability = db.StringField(max_length=20, choices=AVAILABILITY,
        default=None, verbose_name='Is the document freely available?')

    languages = db.ListField(db.StringField(choices=LANGUAGES), default=None,
        verbose_name='In which languages is the document available?')

    url = db.URLField(default=None, verbose_name='URL')

    filename = db.StringField(max_length=128, default=None)

    spatial = db.StringField(max_length=3, choices=YES_NO, default='no',
        verbose_name='Spatial specificity')

    spatial_scale = db.StringField(max_length=128, choices=SPATIAL_SCALE,
        default=None, verbose_name='Spatial scale')

    countries = db.StringField(max_length=128, choices=COUNTRIES, default=None)

    content = db.ListField(db.StringField(), default=None)

    key_elements = db.ListField(db.StringField(choices=KEY_ELEMENTS),
        default=None, verbose_name='Which key elements of ecosystem assessment are documented? ')

    # ecosystems = db.StringField(max_length=3, choices=YES_NO, default='no')

    # ecosystem_types = db.ListField(db.StringField(), default=None)

    # ecosystem_services = db.StringField(max_length=3, choices=YES_NO, default='no')

    # ecosystem_services_types = db.ListField(db.StringField(), default=None)

    feedback = db.StringField(default=None)

