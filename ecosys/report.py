from flask import views
from flask import Blueprint


report = Blueprint('report', __name__)


QUESTIONS = ('origin',)


def initialize_app(app):
    app.register_blueprint(report)


class Report(views.MethodView):

    def get(self):
        return 'report'


report.add_url_rule('/report', view_func=Report.as_view('report'))
