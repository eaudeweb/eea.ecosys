#!/usr/bin/env python

import os

from flask.ext import script
from path import path

from ecosys.middlewares import ReverseProxied
from ecosys.app import create_app
from ecosys.management.commands import ApiRequest
from ecosys.management.commands import CountryRequest


PROJECT_ROOT = os.environ.get('PROJECT_ROOT', os.getcwd())


app = create_app(instance_path=path(PROJECT_ROOT) / 'instance')
app.wsgi_app = ReverseProxied(app.wsgi_app)


def main():
    global app
    manager = script.Manager(app)
    manager.add_command('api_request', ApiRequest())
    manager.add_command('country_request', CountryRequest())
    manager.run()


if __name__ == '__main__':
    main()
