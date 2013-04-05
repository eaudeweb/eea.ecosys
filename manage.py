#!/usr/bin/env python

from flask.ext import script
from middlewares import ReverseProxied
from path import path

from ecosys.app import create_app


PROJECT_ROOT = path(__file__).parent.abspath()


app = create_app(instance_path=PROJECT_ROOT / 'instance')
app.wsgi_app = ReverseProxied(app.wsgi_app)
manager = script.Manager(app)


if __name__ == '__main__':
    manager.run()
