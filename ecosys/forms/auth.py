from flask.ext import wtf
from ecosys.models import User
from ecosys.model_data import COUNTRIES

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

    country = wtf.SelectField(choices=COUNTRIES,
                              validators=[wtf.validators.Required()])

    def save(self, user):
        defaults = self.data
        user.first_name = self.data['first_name']
        user.last_name = self.data['last_name']
        user.phone_number = self.data['phone_number']
        user.organisation = self.data['organisation']
        user.country = self.data['country']
        user.save()
        return user
