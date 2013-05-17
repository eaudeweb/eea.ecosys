from flask.ext import wtf
from ecosys.models import User
from ecosys.model_data import COUNTRIES, ORGANISATION_TYPES
from ecosys.forms.fields import TextInputWithAttributes

class LoginForm(wtf.Form):

    username = wtf.TextField('User ID', validators=[wtf.validators.Required()])

    password = wtf.PasswordField('Password',
                                 validators=[wtf.validators.Required()])


class ProfileForm(wtf.Form):

    first_name = wtf.TextField('First Name',
                               validators=[wtf.validators.Required()])

    last_name = wtf.TextField('Last Name',
                              validators=[wtf.validators.Required()])

    phone_number = wtf.TextField('Phone Number')

    organisation = wtf.TextField('Organisation',
                                 validators=[wtf.validators.Required()])

    country = wtf.SelectField(choices=(('EU', 'Europe'),) + COUNTRIES,
                              validators=[wtf.validators.Required()])

    field_of_expertise = wtf.TextField('Field of expertise')

    organisation_type = wtf.SelectMultipleField('Type of organisation',
                                     choices=ORGANISATION_TYPES,
                                     validators=[wtf.validators.Required()])

    organisation_type_other = wtf.TextField(widget=TextInputWithAttributes(attr={
        'data-placeholder': 'or type different type(s) of organisation here'}))


    def save(self, user):
        defaults = self.data
        user.first_name = self.data['first_name']
        user.last_name = self.data['last_name']
        user.phone_number = self.data['phone_number']
        user.organisation = self.data['organisation']
        user.country = self.data['country']
        user.field_of_expertise = self.data['field_of_expertise']

        organisation_type = self.data['organisation_type']
        organisation_type_other = self.data['organisation_type_other'].split(',')
        if organisation_type_other:
            organisation_type.extend(organisation_type_other)
        user.organisation_type = organisation_type

        user.save()
        return user
