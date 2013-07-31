from flask.ext.script import Command
from ecosys.models import Author


class MigrateAuthors(Command):

    """
    Migrate name to first_name, last_name
    """

    def run(self):
        for author in Author.objects.all():
            split_name = author.name.split(',')
            if len(split_name) == 2:
                last_name, first_name = split_name
                author.last_name = last_name
                author.first_name = first_name
            else:
                author.last_name = author.name
            author.save()
