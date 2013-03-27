from flask.ext import wtf

from libs import markup
from libs.markup import oneliner as e


class EcosystemTableWidget():

    def __call__(self, form_field, **kwargs):
        fields = [f for f in form_field if 'csrf_token' not in f.id ]

        page = markup.page()
        page.table(id='ecosystem-types', class_='ecosystem-types ecosystem')

        page.thead()
        page.tr()
        page.th('', class_='category-left')
        page.th([f.label.text for f in fields])
        page.tr.close()
        page.thead.close()

        page.tbody()

        page.tr(e.th('Issues', colspan=form_field.COLSPAN, class_='category'))
        page.tr()
        page.td(e.div(form_field.ECOSYSTEM_ISSUES_FORM_DATA, class_='category-left'))
        for field in fields:
            field.choices = [(k, v) for k, v in form_field.ECOSYSTEM_ISSUES_FORM]
            page.td(field(**kwargs), class_='check-column')
        page.tr.close()

        page.tr(e.th('Methods', colspan=form_field.COLSPAN, class_='category'))
        page.tr()
        page.td(e.div(form_field.ECOSYSTEM_METHODS_FORM_DATA, class_='category-left'))
        for field in fields:
            field.choices = [(k, v) for k, v in form_field.ECOSYSTEM_METHODS_FORM]
            page.td(field(**kwargs), class_='check-column')
        page.tr.close()

        page.tbody.close()
        page.table.close()

        return page

class EcosystemServiceTableWidget():

    def __call__(self, form_field, **kwargs):
        fields = [f for f in form_field if 'csrf_token' not in f.id ]

        page = markup.page()
        page.table(id='ecosystem-service-types', class_='ecosystem-setvice-types ecosystem')

        page.thead()
        page.tr()
        page.th('', class_='category-left')
        page.th([f.label.text for f in fields])
        page.tr.close()
        page.thead.close()

        page.tbody()
        page.tr(e.th('Type of ecosystems', colspan=form_field.COLSPAN, class_='category'))
        page.tr()
        page.td(e.div(form_field.ECOSYSTEM_TYPES_FORM_DATA, class_='category-left'))
        for field in fields:
            page.td(field(**kwargs), class_='check-column')
        page.tr.close()

        page.tbody.close()
        page.table.close()

        return page


class MultiCheckboxField(wtf.SelectMultipleField):

    def __init__(self, *args, **kwargs):
        pre_validate = kwargs.pop('pre_validate', True)
        super(MultiCheckboxField, self).__init__(*args, **kwargs)

        if not pre_validate:
            self.pre_validate = lambda x: True

    widget = wtf.widgets.ListWidget(prefix_label=False)

    option_widget = wtf.widgets.CheckboxInput()


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
