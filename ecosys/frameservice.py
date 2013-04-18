import re
import time
import requests

from flask.ext import login as flask_login


frame = None
last_hit = None
TIMEOUT = 3600 #seconds
FRAME_URL = 'http://biodiversity.europa.eu/ecosystem-assessments/frame'
MARKER = '<!--SITE_HEADERFOOTER_MARKER-->'


def get_frame_contents():
    """ Simply http-request the html produced by Zope """
    tries = 3
    while tries:
        resp = requests.get(FRAME_URL)
        if resp.status_code == 200:
            return resp.text
        tries -= 1
    return None


def prepare_frame(frame_contents):
    """ Make it extendable by layout template in our app """
    assert MARKER in frame_contents
    baseurl = FRAME_URL.rsplit('/', 1)[0]
    login_re = r"<a href=\"[^>]+>login</a>"

    frame_contents = frame_contents.replace(MARKER, '{% block frame_content %}{% endblock %}')\
        .replace('</title>', '{% block frame_title %}{% endblock %}</title>')\
        .replace('</head>', '{% block head %}{% endblock %}</head>')
    return re.sub(login_re, '{% block login %}{% endblock %}', frame_contents,
                  flags=re.IGNORECASE)


def load_template(name):
    global frame, last_hit
    if name is not 'frame':
        return None
    if frame is None or time.time() - last_hit > TIMEOUT:
        html = get_frame_contents()
        frame = prepare_frame(html)
        last_hit = time.time()

    return frame
