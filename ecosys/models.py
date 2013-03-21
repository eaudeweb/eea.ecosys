from flask.ext.mongoengine import MongoEngine


db = MongoEngine()


class Authors(db.Document):
    name = db.StringField(max_length=128)