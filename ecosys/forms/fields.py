from flask.ext import wtf
from werkzeug import FileStorage

from libs import markup
from libs.markup import oneliner as e


class EcosystemBaseWidget(object):

    def __init__(self, *args, **kwargs):
        self.label = kwargs.pop('label', '')
        self.title = kwargs.pop('title', '')

    def update_data(self, form_field, data):
        for value in form_field.data.values():
            if not value: continue
            for item in value:
                if item not in [i[0] for i in data]: data.append((item, item))
        return data

    def update_keys(self, form_field, data_keys):
        for value in form_field.data.values():
            if not value: continue
            for item in value:
                if item not in data_keys: data_keys.append(item)
        return data_keys


class EcosystemTableWidget(EcosystemBaseWidget):

    def __init__(self, data, categ, **kwargs):
        super(EcosystemTableWidget, self).__init__(self, data, categ, **kwargs)
        self.data, self.categ = data, categ
        self.header = kwargs.pop('header', True)

    def __call__(self, form_field, **kwargs):
        fields = [f for f in form_field if 'csrf_token' not in f.id ]
        data_keys = [i[0] for i in self.data]
        data_keys = self.update_keys(form_field, data_keys)
        self.data = self.update_data(form_field, self.data)

        page = markup.page()
        page.label(self.label)
        page.table(id='ecosystem-types-%s' % self.categ.lower(),
                   class_='ecosystem-types ecosystem')

        if self.header:
            page.thead()
            page.tr()
            page.th('', class_='category-left')
            for i, f in enumerate(fields):
                page.th(f.label.text, class_=i%2 and 'odd' or 'even')
            page.tr.close()
            page.thead.close()

        page.tbody()

        page.tr(e.th(self.categ, colspan=form_field.COLSPAN, class_='category'))
        page.tr()
        page.td(e.div(data_keys), class_='category-left')

        for i, field in enumerate(fields):
            field.choices = [(k, v) for k, v in self.data]
            odd_even = i%2 and 'odd' or 'even'
            page.td(field(**kwargs), class_=('check-column %s' % odd_even))

        page.tr.close()
        page.tbody.close()
        page.table.close()

        return page


class EcosystemServiceTableWidget(EcosystemBaseWidget):

    def __init__(self, data, *args, **kwargs):
        super(EcosystemServiceTableWidget, self).__init__(self, *args, **kwargs)
        self.data = data

    def __call__(self, form_field, **kwargs):
        fields = [f for f in form_field if 'csrf_token' not in f.id ]
        data_keys = [i[0] for i in self.data]
        data_keys = self.update_keys(form_field, data_keys)
        self.data = self.update_data(form_field, self.data)

        page = markup.page()
        page.label(self.label)
        page.table(id='ecosystem-service-types', class_='ecosystem-service-types ecosystem')

        page.thead()
        page.tr()
        page.th('', class_='category-left')
        for i, f in enumerate(fields):
            page.th(f.label.text, class_=i%2 and 'odd' or 'even')
        page.tr.close()
        page.thead.close()

        page.tbody()
        page.tr(e.th('Type of ecosystems', colspan=form_field.COLSPAN, class_='category'))
        page.tr()
        page.td(e.div(data_keys), class_='category-left')
        for i, field in enumerate(fields):
            field.choices = [(k, v) for k, v in self.data]
            odd_even = i%2 and 'odd' or 'even'
            page.td(field(**kwargs), class_=('check-column %s' % odd_even))
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


class MultipleFileField(wtf.FileField):

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [v for v in valuelist if v]
        else:
            self.data = []

    def has_file(self):
        if self.data and isinstance(self.data, list):
            for item in self.data:
                if not isinstance(item, FileStorage):
                    return False

            return True
        else:
            return False


class MultipleFileAllowed(wtf.FileAllowed):

    def __call__(self, form, field):
        if not field.has_file():
            return
        data = field.data
        if data and isinstance(data, list):
            for item in data:
                if not self.upload_set.file_allowed(item, item.filename):
                    raise wtf.ValidationError(self.message)
        else:
            raise wtf.ValidationError(self.message)


class CustomBoolean(wtf.SelectField):
    pass


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
        if not field.data == 'Yes':
            return True
        for f in self.fields:
            required_field = getattr(form, f, None)
            if required_field and required_field.data:
                continue
            else:
                raise wtf.ValidationError(self.message)


class TextInputWithAttributes(wtf.widgets.TextInput):

    def __init__(self, *args, **kwargs):
        self.attr = kwargs.pop('attr', {})
        super(TextInputWithAttributes, self).__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        for k, v in self.attr.items():
            kwargs[k] = v
        return super(TextInputWithAttributes, self).__call__(field, **kwargs)

