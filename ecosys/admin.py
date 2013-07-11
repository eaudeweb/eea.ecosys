from flask.ext import superadmin, login as flask_login
from ecosys import models


class AdminLogin():

    def is_accessible(self):
        user = flask_login.current_user
        if user.is_authenticated() and 'administrator' in user.roles:
            return True
        return False


class AdminIndex(AdminLogin, superadmin.AdminIndexView):
    pass


class AuthorAdmin(AdminLogin, superadmin.model.ModelAdmin):
    pass


class OrganisationAdmin(AdminLogin, superadmin.model.ModelAdmin):
    pass


class OrganizerAdmin(AdminLogin, superadmin.model.ModelAdmin):
    pass


class UserAdmin(AdminLogin, superadmin.model.ModelAdmin):

    readonly_fields = ('id',)


class FeedbackAdmin(AdminLogin, superadmin.model.ModelAdmin):
    pass


admin = superadmin.Admin(index_view=AdminIndex())

admin.register(models.Author, AuthorAdmin)

admin.register(models.Organisation, OrganisationAdmin)

admin.register(models.Organizer, OrganizerAdmin)

admin.register(models.User, UserAdmin)

admin.register(models.Feedback, FeedbackAdmin)
