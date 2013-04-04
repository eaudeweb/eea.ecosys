import re
from setuptools import setup


setup(
    name='ecosys',
    version='1.0',
    url='https://github.com/eaudeweb/eea.ecosys',
    license='Mozilla Public License',
    author='Eau de Web',
    author_email='office@eaudeweb.ro',
    description='Virtual Library for Ecosystem Assessments in Europe',
    py_modules=['ecosys'],
    zip_safe=False,
    platforms='any',
    install_requires=['Flask==0.9',
                      'Jinja2==2.6',
                      'Werkzeug==0.8.3',
                      'Flask-Script==0.5.3',
                      'Flask-WTF==0.8.3',
                      'Flask-Assets==0.8',
                      'Flask-Uploads==0.1.3',
                      'Flask-Login==0.1.3',
                      'webassets==0.8',
                      'pymongo==2.4.2',
                      'mongoengine==0.7.9',
                      'WTForms==1.0.3',
                      'path.py==3.0.1',
                      'requests==1.1.0',
                      'python-ldap==2.4.10',
                    ],
    dependency_links=['https://github.com/eaudeweb/flask-mongoengine/archive/master.zip'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)