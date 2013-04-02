import time
import requests
import flask

frame = None
last_hit = None
TIMEOUT = 3600 #seconds
MARKER = '<!--SITE_HEADERFOOTER_MARKER-->'

def get_frame_contents(url):
    """ Simply http-request the html produced by Zope """
    tries = 3
    while tries:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text
        tries -= 1
    return None

def prepare_frame(frame_contents, baseurl):
    """ Make it extendable by layout template in our app """
    assert MARKER in frame_contents
    return frame_contents.replace(MARKER, '{% block frame_content %}{% endblock %}')\
        .replace('<title>Ecosystem Assessments in Europe - </title>',
                 '<title>Ecosystem Assessments in Europe - {% block title %}{% endblock %}</title>')\
        .replace('</head>', '{% block head %}{% endblock %}</head>')\
        .replace('<img src="images', '<img src="%s/images' % baseurl)

def load_template(name):
    global frame, last_hit
    if name is not 'frame':
        return None
    if frame is None or time.time() - last_hit > TIMEOUT:
        url = flask.current_app.config['FRAME_URL']
        html = get_frame_contents(url)
        frame = prepare_frame(html, url.rsplit('/', 1)[0])
        last_hit = time.time()

    return frame
