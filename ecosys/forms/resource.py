from flask.ext import wtf
from flask.ext.mongoengine.wtf import model_form
from ecosys import models


_AuthorForm = model_form(models.Author)
_OrganisationForm = model_form(models.Organisation)


class AuthorForm(_AuthorForm):
    pass


class OrganisationForm(_OrganisationForm):
    pass
