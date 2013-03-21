from flask.ext.mongoengine import MongoEngine
from ecosys.model_data import *

db = MongoEngine()


class Authors(db.Document):

    name = db.StringField(max_length=128, required=True)


class Organisations(db.Document):

    name = db.StringField(max_length=128, required=True)


class Organizers(db.Document):

    name = db.StringField(max_length=128, required=True)



class Resource(db.Document):

    title = db.StringField(max_length=512, required=True)

    english_title = db.StringField(max_length=512)

    language = db.StringField(choices=LANGUAGES, required=True)

    resource_type = db.StringField(max_length=20, required=True,
                                   choices=RESOURCE_TYPES)

    authors = db.ListField(db.ReferenceField(Authors), default=None)

    organisations = db.ListField(db.ReferenceField(Organisations), default=None)

    organizers = db.ListField(db.ReferenceField(Organizers), default=None)

    year_of_publication = db.IntField(min_value=0, default=None)

    reviews = db.ListField(db.GenericEmbeddedDocumentField())


class LiteratureReview(db.EmbeddedDocument):

    origin = db.ListField(db.StringField(), default=None)

    status = db.StringField(choices=STATUS, default=None)

    availability = db.StringField(max_length=20, choices=AVAILABILITY,
                                  default=None)

    languages = db.ListField(db.StringField(choices=LANGUAGES), default=None)

    url = db.URLField(default=None)

    filename = db.StringField(max_length=128, default=None)

    spatial = db.StringField(max_length=3, choices=YES_NO, default='no')

    spatial_scale = db.StringField(max_length=128, choices=SPATIAL_SCALE,
                                   default=None)

    countries = db.StringField(max_length=128, choices=COUNTRIES, default=None)

    content = db.ListField(db.StringField(), default=None)

    key_elements = db.ListField(db.StringField(choices=KEY_ELEMENTS), default=None)

    ecosystems = db.StringField(max_length=3, choices=YES_NO, default='no')

    ecosystem_types = db.ListField(db.StringField(), default=None)

    ecosystem_services = db.StringField(max_length=3, choices=YES_NO, default='no')

    ecosystem_services_types = db.ListField(db.StringField(), default=None)

    feedback = db.StringField(default=None)

